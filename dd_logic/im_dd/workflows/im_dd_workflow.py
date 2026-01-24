"""
IM DDワークフロー

PDFから財務諸表を抽出し、既存のDCF分析ロジックを使用してIM DD評価を実行します。
"""
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any, List
from datetime import datetime

# 既存のDCF分析ロジックをインポート
from dd_logic.im_dd.calculations.dcf_analysis import (
    calculate_dcf,
    calculate_terminal_value,
    calculate_wacc,
    sensitivity_analysis
)

# 抽出モジュールをインポート
from dd_logic.im_dd.extractors.financial_statement_extractor import FinancialStatementExtractor
from dd_logic.common.pdf_parser import extract_text_from_pdf

logger = logging.getLogger(__name__)


class IMDDWorkflow:
    """IM DDワークフロークラス"""
    
    def __init__(self, deal_dir: str):
        """
        IMDDWorkflowを初期化
        
        Args:
            deal_dir: 案件ディレクトリのパス（deals/[deal_name]）
        """
        self.deal_dir = Path(deal_dir)
        self.im_dir = self.deal_dir / "im"
        self.output_dir = self.deal_dir / "dd_results" / "im_dd"
        
        # 出力ディレクトリを作成
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process(self) -> Dict[str, Any]:
        """
        IM DDワークフローを実行
        
        Returns:
            処理結果の辞書
        """
        logger.info(f"IM DDワークフロー開始: {self.deal_dir}")
        
        # 1. PDFファイルを検出
        pdf_files = self._find_pdf_files()
        if not pdf_files:
            logger.warning("PDFファイルが見つかりませんでした")
            return {"status": "error", "message": "PDFファイルが見つかりません"}
        
        # 2. 財務諸表を抽出
        financial_statements = {}
        text_content = ""
        
        for pdf_path in pdf_files:
            logger.info(f"PDFファイルを処理: {pdf_path}")
            try:
                extractor = FinancialStatementExtractor(str(pdf_path))
                statements = extractor.extract_all_statements()
                financial_statements.update(statements)
                
                # テキストも抽出
                text_content += extract_text_from_pdf(str(pdf_path))
            except Exception as e:
                logger.error(f"PDF処理エラー: {e}")
        
        # 3. 財務諸表データを基に分析
        analysis_result = self._analyze_financial_statements(financial_statements)
        
        # 4. DCF分析を実行（可能な場合）
        dcf_result = self._run_dcf_analysis(financial_statements)
        
        # 5. 評価結果を生成
        evaluation_result = self._evaluate(financial_statements, analysis_result, dcf_result, text_content)
        
        # 6. レポートを生成
        report_path = self._generate_report(evaluation_result, financial_statements, dcf_result)
        
        # 7. データをJSONで保存
        data_path = self._save_data(evaluation_result, financial_statements, dcf_result)
        
        logger.info(f"IM DDワークフロー完了: {report_path}")
        
        return {
            "status": "success",
            "report_path": str(report_path),
            "data_path": str(data_path),
            "result": evaluation_result
        }
    
    def _find_pdf_files(self) -> List[Path]:
        """
        PDFファイルを検出
        
        Returns:
            見つかったPDFファイルのリスト
        """
        files = []
        
        if not self.im_dir.exists():
            logger.warning(f"IMディレクトリが存在しません: {self.im_dir}")
            return files
        
        # PDFファイルを検索
        pdf_files = list(self.im_dir.glob("**/*.pdf"))
        files.extend(pdf_files)
        
        logger.info(f"PDFファイルを検出: {len(files)}件")
        return files
    
    def _analyze_financial_statements(
        self, 
        financial_statements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        財務諸表データを分析
        
        Args:
            financial_statements: 抽出した財務諸表データ
        
        Returns:
            分析結果の辞書
        """
        logger.info("財務諸表を分析中...")
        
        analysis = {
            "balance_sheet_analysis": {},
            "income_statement_analysis": {},
            "cash_flow_analysis": {}
        }
        
        # 貸借対照表の分析
        if financial_statements.get('balance_sheet'):
            bs_data = financial_statements['balance_sheet'].get('data', {})
            analysis["balance_sheet_analysis"] = self._analyze_balance_sheet(bs_data)
        
        # 損益計算書の分析
        if financial_statements.get('income_statement'):
            pl_data = financial_statements['income_statement'].get('data', {})
            analysis["income_statement_analysis"] = self._analyze_income_statement(pl_data)
        
        # キャッシュフロー計算書の分析
        if financial_statements.get('cash_flow'):
            cf_data = financial_statements['cash_flow'].get('data', {})
            analysis["cash_flow_analysis"] = self._analyze_cash_flow(cf_data)
        
        return analysis
    
    def _analyze_balance_sheet(self, bs_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        貸借対照表を分析
        
        Args:
            bs_data: 貸借対照表データ
        
        Returns:
            分析結果
        """
        result = {}
        
        # 主要項目を抽出
        cash = bs_data.get('cash', {}).get('latest_value')
        debt = bs_data.get('interest_bearing_debt', {}).get('latest_value')
        equity = bs_data.get('equity', {}).get('latest_value')
        
        if cash is not None:
            result['cash'] = cash
        if debt is not None:
            result['debt'] = debt
        if equity is not None:
            result['equity'] = equity
        
        # Net Debtを計算
        if cash is not None and debt is not None:
            result['net_debt'] = debt - cash
        
        return result
    
    def _analyze_income_statement(self, pl_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        損益計算書を分析
        
        Args:
            pl_data: 損益計算書データ
        
        Returns:
            分析結果
        """
        result = {}
        
        # 主要項目を抽出
        revenue = pl_data.get('revenue', {}).get('latest_value')
        ebitda = pl_data.get('ebitda', {}).get('latest_value')
        net_income = pl_data.get('net_income', {}).get('latest_value')
        
        if revenue is not None:
            result['revenue'] = revenue
        if ebitda is not None:
            result['ebitda'] = ebitda
        if net_income is not None:
            result['net_income'] = net_income
        
        # EBITDAマージンを計算
        if revenue is not None and ebitda is not None and revenue > 0:
            result['ebitda_margin'] = (ebitda / revenue) * 100
        
        return result
    
    def _analyze_cash_flow(self, cf_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        キャッシュフロー計算書を分析
        
        Args:
            cf_data: キャッシュフロー計算書データ
        
        Returns:
            分析結果
        """
        result = {}
        
        # 主要項目を抽出
        operating_cf = cf_data.get('operating_cf', {}).get('latest_value')
        free_cash_flow = cf_data.get('free_cash_flow', {}).get('latest_value')
        
        if operating_cf is not None:
            result['operating_cf'] = operating_cf
        if free_cash_flow is not None:
            result['free_cash_flow'] = free_cash_flow
        
        return result
    
    def _run_dcf_analysis(
        self, 
        financial_statements: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        DCF分析を実行
        
        Args:
            financial_statements: 抽出した財務諸表データ
        
        Returns:
            DCF分析結果（実行できない場合はNone）
        """
        logger.info("DCF分析を実行中...")
        
        # キャッシュフロー計算書からFCFを取得
        cf_data = financial_statements.get('cash_flow', {}).get('data', {})
        fcf_data = cf_data.get('free_cash_flow', {})
        
        if not fcf_data or not fcf_data.get('values'):
            logger.warning("FCFデータが不足しているため、DCF分析をスキップします")
            return None
        
        # FCFのリストを取得（過去から未来への順序を想定）
        fcf_values = fcf_data['values']
        
        if len(fcf_values) < 2:
            logger.warning("FCFデータが不足しているため、DCF分析をスキップします")
            return None
        
        # デフォルト値を使用（実際の実装では、より適切な値を設定）
        discount_rate = 0.10  # 10%
        terminal_growth_rate = 0.03  # 3%
        
        # ターミナルバリューを計算
        final_fcf = fcf_values[-1]
        terminal_value = calculate_terminal_value(
            final_fcf,
            terminal_growth_rate,
            discount_rate
        )
        
        # DCF分析を実行
        dcf_result = calculate_dcf(
            fcf_values,
            terminal_value,
            discount_rate,
            terminal_growth_rate
        )
        
        return dcf_result
    
    def _evaluate(
        self,
        financial_statements: Dict[str, Any],
        analysis_result: Dict[str, Any],
        dcf_result: Optional[Dict[str, Any]],
        text_content: str
    ) -> Dict[str, Any]:
        """
        評価を実行
        
        Args:
            financial_statements: 財務諸表データ
            analysis_result: 分析結果
            dcf_result: DCF分析結果
            text_content: テキスト内容
        
        Returns:
            評価結果の辞書
        """
        logger.info("評価を実行中...")
        
        # 簡易的な評価（実際の実装では、より詳細な評価ロジックを実装）
        evaluation = {
            "business_evaluation": {
                "score": 70,
                "evaluation": "良好",
                "details": "事業性は良好です",
                "comments": ""
            },
            "financial_evaluation": {
                "score": 75,
                "evaluation": "良好",
                "details": "財務状況は良好です",
                "comments": "",
                "dcf_analysis": dcf_result
            },
            "management_evaluation": {
                "score": 65,
                "evaluation": "普通",
                "details": "経営陣評価",
                "comments": ""
            },
            "risk_evaluation": {
                "score": 60,
                "evaluation": "注意",
                "details": "リスク評価",
                "comments": "",
                "risk_factors": []
            },
            "investment_terms_evaluation": {
                "score": 70,
                "evaluation": "良好",
                "details": "投資条件評価",
                "comments": ""
            }
        }
        
        # 総合スコアを計算（簡易版）
        scores = [
            evaluation["business_evaluation"]["score"],
            evaluation["financial_evaluation"]["score"],
            evaluation["management_evaluation"]["score"],
            evaluation["risk_evaluation"]["score"],
            evaluation["investment_terms_evaluation"]["score"]
        ]
        total_score = sum(scores) / len(scores)
        
        evaluation["total_score"] = total_score
        evaluation["investment_recommendation"] = "推奨" if total_score >= 70 else "要検討"
        evaluation["key_risks"] = []
        
        return evaluation
    
    def _generate_report(
        self,
        evaluation_result: Dict[str, Any],
        financial_statements: Dict[str, Any],
        dcf_result: Optional[Dict[str, Any]]
    ) -> Path:
        """
        レポートを生成
        
        Args:
            evaluation_result: 評価結果
            financial_statements: 財務諸表データ
            dcf_result: DCF分析結果
        
        Returns:
            生成されたレポートファイルのパス
        """
        logger.info("レポートを生成中...")
        
        # レポートテンプレートを読み込み
        template_path = Path(__file__).parent.parent / "outputs" / "report_template.md"
        
        if template_path.exists():
            template = template_path.read_text(encoding='utf-8')
            report = self._fill_template(template, evaluation_result, financial_statements, dcf_result)
        else:
            # 簡易レポートを生成
            report = self._generate_simple_report(evaluation_result, financial_statements, dcf_result)
        
        # レポートを保存
        report_path = self.output_dir / "report.md"
        report_path.write_text(report, encoding='utf-8')
        
        return report_path
    
    def _fill_template(
        self,
        template: str,
        evaluation_result: Dict[str, Any],
        financial_statements: Dict[str, Any],
        dcf_result: Optional[Dict[str, Any]]
    ) -> str:
        """
        テンプレートを埋め込む
        
        Args:
            template: テンプレート文字列
            evaluation_result: 評価結果
            financial_statements: 財務諸表データ
            dcf_result: DCF分析結果
        
        Returns:
            埋め込まれたレポート文字列
        """
        report = template
        
        # 案件情報
        deal_name = self.deal_dir.name
        report = report.replace('[案件名]', deal_name)
        report = report.replace('[評価日]', datetime.now().strftime('%Y-%m-%d'))
        
        # 評価結果サマリー
        total_score = evaluation_result.get('total_score', 0)
        recommendation = evaluation_result.get('investment_recommendation', '不明')
        report = report.replace('[スコア]', f"{total_score:.1f}")
        report = report.replace('[推奨度]', recommendation)
        
        # 各論点の評価結果を埋め込む（簡易版）
        # 実際の実装では、より詳細な置換が必要
        
        return report
    
    def _generate_simple_report(
        self,
        evaluation_result: Dict[str, Any],
        financial_statements: Dict[str, Any],
        dcf_result: Optional[Dict[str, Any]]
    ) -> str:
        """
        簡易レポートを生成
        
        Args:
            evaluation_result: 評価結果
            financial_statements: 財務諸表データ
            dcf_result: DCF分析結果
        
        Returns:
            生成されたレポート文字列
        """
        report_lines = [
            f"# IM DD評価結果レポート",
            f"",
            f"## 案件情報",
            f"- **案件名**: {self.deal_dir.name}",
            f"- **評価日**: {datetime.now().strftime('%Y-%m-%d')}",
            f"",
            f"## 評価結果サマリー",
            f"- **総合スコア**: {evaluation_result.get('total_score', 0):.1f}",
            f"- **投資推奨度**: {evaluation_result.get('investment_recommendation', '不明')}",
            f"",
            f"## 詳細データ",
            f"",
            f"```json",
            json.dumps(evaluation_result, ensure_ascii=False, indent=2),
            f"```",
        ]
        
        if dcf_result:
            report_lines.extend([
                f"",
                f"## DCF分析結果",
                f"",
                f"```json",
                json.dumps(dcf_result, ensure_ascii=False, indent=2),
                f"```",
            ])
        
        return '\n'.join(report_lines)
    
    def _save_data(
        self,
        evaluation_result: Dict[str, Any],
        financial_statements: Dict[str, Any],
        dcf_result: Optional[Dict[str, Any]]
    ) -> Path:
        """
        データをJSONで保存
        
        Args:
            evaluation_result: 評価結果
            financial_statements: 財務諸表データ
            dcf_result: DCF分析結果
        
        Returns:
            保存されたデータファイルのパス
        """
        data = {
            "evaluation_result": evaluation_result,
            "financial_statements": financial_statements,
            "dcf_result": dcf_result,
            "timestamp": datetime.now().isoformat()
        }
        
        data_path = self.output_dir / "data.json"
        data_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        return data_path


def run_im_dd_workflow(deal_dir: str) -> Dict[str, Any]:
    """
    IM DDワークフローを実行する簡易関数
    
    Args:
        deal_dir: 案件ディレクトリのパス
    
    Returns:
        処理結果の辞書
    """
    workflow = IMDDWorkflow(deal_dir)
    return workflow.process()

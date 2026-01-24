"""
NN DDワークフロー

PDF/MDファイルを読み込み、既存の計算ロジックを使用してNN DD評価を実行します。
"""
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime

# 既存の計算ロジックをインポート
from dd_logic.nn_dd.calculations.nn_dd_calculator import NNDDCalculator

# 抽出モジュールをインポート
from dd_logic.nn_dd.extractors.simple_financial_extractor import SimpleFinancialExtractor
from dd_logic.common.pdf_parser import extract_text_from_pdf

logger = logging.getLogger(__name__)


class NNDDWorkflow:
    """NN DDワークフロークラス"""
    
    def __init__(self, deal_dir: str):
        """
        NNDDWorkflowを初期化
        
        Args:
            deal_dir: 案件ディレクトリのパス（deals/[deal_name]）
        """
        self.deal_dir = Path(deal_dir)
        self.nn_dir = self.deal_dir / "nn"
        self.output_dir = self.deal_dir / "dd_results" / "nn_dd"
        
        # 出力ディレクトリを作成
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.calculator = NNDDCalculator()
    
    def process(self) -> Dict[str, Any]:
        """
        NN DDワークフローを実行
        
        Returns:
            処理結果の辞書
        """
        logger.info(f"NN DDワークフロー開始: {self.deal_dir}")
        
        # 1. ファイルを検出
        files = self._find_input_files()
        if not files:
            logger.warning("入力ファイルが見つかりませんでした")
            return {"status": "error", "message": "入力ファイルが見つかりません"}
        
        # 2. ファイルを読み込み
        financial_data = {}
        qualitative_data = {}
        text_content = ""
        
        for file_path in files:
            if file_path.suffix.lower() == '.pdf':
                # PDFファイルの処理
                pdf_data = self._process_pdf(file_path)
                financial_data.update(pdf_data.get('financial', {}))
                text_content += pdf_data.get('text', '')
            elif file_path.suffix.lower() == '.md':
                # Markdownファイルの処理
                md_data = self._process_markdown(file_path)
                financial_data.update(md_data.get('financial', {}))
                qualitative_data.update(md_data.get('qualitative', {}))
                text_content += md_data.get('text', '')
        
        # 3. 定性情報が抽出されていない場合は、テキストから抽出を試みる
        if not qualitative_data and text_content:
            qualitative_data = self._extract_qualitative_from_text(text_content)
        
        # 4. 計算を実行
        calculation_result = self._run_calculation(financial_data, qualitative_data)
        
        # 5. レポートを生成
        report_path = self._generate_report(calculation_result, financial_data, qualitative_data)
        
        # 6. データをJSONで保存
        data_path = self._save_data(calculation_result, financial_data, qualitative_data)
        
        logger.info(f"NN DDワークフロー完了: {report_path}")
        
        return {
            "status": "success",
            "report_path": str(report_path),
            "data_path": str(data_path),
            "result": calculation_result
        }
    
    def _find_input_files(self) -> list[Path]:
        """
        入力ファイルを検出
        
        Returns:
            見つかったファイルのリスト
        """
        files = []
        
        if not self.nn_dir.exists():
            logger.warning(f"NNディレクトリが存在しません: {self.nn_dir}")
            return files
        
        # PDFファイルを検索
        pdf_files = list(self.nn_dir.glob("**/*.pdf"))
        files.extend(pdf_files)
        
        # Markdownファイルを検索
        md_files = list(self.nn_dir.glob("**/*.md"))
        files.extend(md_files)
        
        logger.info(f"入力ファイルを検出: {len(files)}件")
        return files
    
    def _process_pdf(self, pdf_path: Path) -> Dict[str, Any]:
        """
        PDFファイルを処理
        
        Args:
            pdf_path: PDFファイルのパス
        
        Returns:
            処理結果の辞書
        """
        logger.info(f"PDFファイルを処理: {pdf_path}")
        
        try:
            # 簡易財務数値抽出
            extractor = SimpleFinancialExtractor(str(pdf_path))
            financial_data = extractor.extract_financial_data()
            
            # テキストも抽出（定性情報抽出用）
            text = extract_text_from_pdf(str(pdf_path))
            
            return {
                "financial": financial_data,
                "text": text
            }
        except Exception as e:
            logger.error(f"PDF処理エラー: {e}")
            return {"financial": {}, "text": ""}
    
    def _process_markdown(self, md_path: Path) -> Dict[str, Any]:
        """
        Markdownファイルを処理
        
        Args:
            md_path: Markdownファイルのパス
        
        Returns:
            処理結果の辞書
        """
        logger.info(f"Markdownファイルを処理: {md_path}")
        
        try:
            text = md_path.read_text(encoding='utf-8')
            
            # テキストから数値データを抽出（簡易版）
            financial_data = self._extract_financial_from_text(text)
            
            # 定性情報を抽出
            qualitative_data = self._extract_qualitative_from_text(text)
            
            return {
                "financial": financial_data,
                "qualitative": qualitative_data,
                "text": text
            }
        except Exception as e:
            logger.error(f"Markdown処理エラー: {e}")
            return {"financial": {}, "qualitative": {}, "text": ""}
    
    def _extract_financial_from_text(self, text: str) -> Dict[str, Optional[float]]:
        """
        テキストから財務数値を抽出（簡易版）
        
        Args:
            text: テキスト内容
        
        Returns:
            抽出した財務数値の辞書
        """
        import re
        
        result = {
            'sales': None,
            'adj_ebitda': None,
            'net_debt': None,
            'ebitda_multiple': None
        }
        
        # 簡易的なパターンマッチング
        patterns = {
            'sales': [r'売上[高]?[:\s]*([\d,]+\.?\d*)', r'revenue[:\s]*([\d,]+\.?\d*)'],
            'adj_ebitda': [r'調整後\s*ebitda[:\s]*([\d,]+\.?\d*)', r'adj\s*ebitda[:\s]*([\d,]+\.?\d*)'],
            'net_debt': [r'net\s*debt[:\s]*([\d,]+\.?\d*)', r'純有利子負債[:\s]*([\d,]+\.?\d*)'],
            'ebitda_multiple': [r'ebitda倍率[:\s]*([\d,]+\.?\d*)', r'ebitda\s*multiple[:\s]*([\d,]+\.?\d*)'],
        }
        
        for key, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        value_str = match.group(1).replace(',', '')
                        result[key] = float(value_str)
                        break
                    except (ValueError, IndexError):
                        continue
        
        return result
    
    def _extract_qualitative_from_text(self, text: str) -> Dict[str, Optional[int]]:
        """
        テキストから定性情報を抽出
        
        Args:
            text: テキスト内容
        
        Returns:
            抽出した定性スコアの辞書
        """
        # 注意: 実際の実装では、AI/LLMを使用してより高度な抽出を行う
        # ここでは簡易的な実装として、テキストからキーワードを探す
        
        result = {
            'fit_score': None,
            'brand_score': None,
            'digital_score': None,
            'scarcity_score': None
        }
        
        # 簡易的なキーワードベースの抽出
        # 実際の実装では、AI/LLMを使用してより正確な抽出を行う
        # ここではプレースホルダーとして実装
        
        return result
    
    def _run_calculation(
        self, 
        financial_data: Dict[str, Optional[float]], 
        qualitative_data: Dict[str, Optional[int]]
    ) -> Dict[str, Any]:
        """
        計算を実行
        
        Args:
            financial_data: 財務データ
            qualitative_data: 定性データ
        
        Returns:
            計算結果の辞書
        """
        logger.info("計算を実行中...")
        
        result = self.calculator.calculate_all(
            sales=financial_data.get('sales'),
            adj_ebitda=financial_data.get('adj_ebitda'),
            net_debt=financial_data.get('net_debt'),
            ebitda_multiple=financial_data.get('ebitda_multiple'),
            fit_score=qualitative_data.get('fit_score'),
            brand_score=qualitative_data.get('brand_score'),
            digital_score=qualitative_data.get('digital_score'),
            scarcity_score=qualitative_data.get('scarcity_score')
        )
        
        return result
    
    def _generate_report(
        self, 
        calculation_result: Dict[str, Any],
        financial_data: Dict[str, Optional[float]],
        qualitative_data: Dict[str, Optional[int]]
    ) -> Path:
        """
        レポートを生成
        
        Args:
            calculation_result: 計算結果
            financial_data: 財務データ
            qualitative_data: 定性データ
        
        Returns:
            生成されたレポートファイルのパス
        """
        logger.info("レポートを生成中...")
        
        # レポートテンプレートを読み込み
        template_path = Path(__file__).parent.parent / "outputs" / "report_template.md"
        if not template_path.exists():
            logger.warning(f"レポートテンプレートが見つかりません: {template_path}")
            # 簡易レポートを生成
            return self._generate_simple_report(calculation_result, financial_data, qualitative_data)
        
        template = template_path.read_text(encoding='utf-8')
        
        # テンプレートを埋め込む
        report = self._fill_template(template, calculation_result, financial_data, qualitative_data)
        
        # レポートを保存
        report_path = self.output_dir / "report.md"
        report_path.write_text(report, encoding='utf-8')
        
        return report_path
    
    def _fill_template(
        self,
        template: str,
        calculation_result: Dict[str, Any],
        financial_data: Dict[str, Optional[float]],
        qualitative_data: Dict[str, Optional[int]]
    ) -> str:
        """
        テンプレートを埋め込む
        
        Args:
            template: テンプレート文字列
            calculation_result: 計算結果
            financial_data: 財務データ
            qualitative_data: 定性データ
        
        Returns:
            埋め込まれたレポート文字列
        """
        # 簡易的な置換（実際の実装ではより高度なテンプレートエンジンを使用）
        report = template
        
        # 案件情報
        deal_name = self.deal_dir.name
        report = report.replace('[案件名]', deal_name)
        report = report.replace('[YYYY-MM-DD]', datetime.now().strftime('%Y-%m-%d'))
        
        # 最終判定
        final_decision = calculation_result.get('final_decision', '不明')
        report = report.replace('[見送り / 見送りでない]', final_decision)
        
        # ゲート判定
        gate_results = calculation_result.get('gate_results', {})
        quant_result = gate_results.get('quantitative', '不明')
        qual_result = gate_results.get('qualitative', '不明')
        report = report.replace('[OK / NG]', quant_result)
        report = report.replace('[合格 / 不合格]', qual_result)
        
        # 数値データの置換（簡易版）
        # 実際の実装では、より詳細な置換が必要
        
        return report
    
    def _generate_simple_report(
        self,
        calculation_result: Dict[str, Any],
        financial_data: Dict[str, Optional[float]],
        qualitative_data: Dict[str, Optional[int]]
    ) -> Path:
        """
        簡易レポートを生成（テンプレートがない場合）
        
        Args:
            calculation_result: 計算結果
            financial_data: 財務データ
            qualitative_data: 定性データ
        
        Returns:
            生成されたレポートファイルのパス
        """
        report_lines = [
            f"# NN DD評価結果レポート",
            f"",
            f"## 案件情報",
            f"- **案件名**: {self.deal_dir.name}",
            f"- **評価日**: {datetime.now().strftime('%Y-%m-%d')}",
            f"",
            f"## 評価結果サマリー",
            f"",
            f"### 最終判定",
            f"- **判定結果**: {calculation_result.get('final_decision', '不明')}",
            f"",
            f"### ゲート判定結果",
            f"- **定量ゲート**: {calculation_result.get('gate_results', {}).get('quantitative', '不明')}",
            f"- **定性ゲート**: {calculation_result.get('gate_results', {}).get('qualitative', '不明')}",
            f"",
            f"## 詳細データ",
            f"",
            f"```json",
            json.dumps(calculation_result, ensure_ascii=False, indent=2),
            f"```",
        ]
        
        report_path = self.output_dir / "report.md"
        report_path.write_text('\n'.join(report_lines), encoding='utf-8')
        
        return report_path
    
    def _save_data(
        self,
        calculation_result: Dict[str, Any],
        financial_data: Dict[str, Optional[float]],
        qualitative_data: Dict[str, Optional[int]]
    ) -> Path:
        """
        データをJSONで保存
        
        Args:
            calculation_result: 計算結果
            financial_data: 財務データ
            qualitative_data: 定性データ
        
        Returns:
            保存されたデータファイルのパス
        """
        data = {
            "calculation_result": calculation_result,
            "financial_data": financial_data,
            "qualitative_data": qualitative_data,
            "timestamp": datetime.now().isoformat()
        }
        
        data_path = self.output_dir / "data.json"
        data_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        return data_path


def run_nn_dd_workflow(deal_dir: str) -> Dict[str, Any]:
    """
    NN DDワークフローを実行する簡易関数
    
    Args:
        deal_dir: 案件ディレクトリのパス
    
    Returns:
        処理結果の辞書
    """
    workflow = NNDDWorkflow(deal_dir)
    return workflow.process()

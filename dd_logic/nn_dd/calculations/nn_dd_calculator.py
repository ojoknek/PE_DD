"""
NN DD計算ロジック - 事業承継ファンド向け

README.mdの仕様に完全準拠した計算システム
"""
from typing import Dict, Optional, Literal, List
from enum import Enum


class Rating(Enum):
    """離散判定の評価ランク"""
    EXCELLENT = "◎"  # 優秀
    GOOD = "〇"      # 良好
    WARNING = "△"    # 注意
    FAIL = "×"       # 不合格
    NO_DATA = "数値未入力"
    EMPTY = "（空欄）"


class GateResult(Enum):
    """ゲート判定結果"""
    OK = "OK"
    NG = "NG"


class FinalDecision(Enum):
    """最終判定"""
    SKIP = "見送り"
    PASS = "見送りでない"


class NNDDCalculator:
    """
    NN DD計算ロジック
    
    README.mdの仕様に基づいて、定量・定性の両面から評価を行います。
    """
    
    def __init__(self):
        """初期化"""
        pass
    
    # ========== 1) 中間計算（Derived Metrics） ==========
    
    def calculate_nd_to_ebitda(
        self, 
        net_debt: Optional[float], 
        adj_ebitda: Optional[float]
    ) -> Optional[float]:
        """
        ND/EBITDA（レバレッジ）を計算
        
        Args:
            net_debt: Net Debt（有利子負債−現預金）
            adj_ebitda: 調整後EBITDA
        
        Returns:
            ND/EBITDA倍率（adj_ebitdaが0または未入力の場合はNone）
        """
        if adj_ebitda is None or adj_ebitda == 0:
            return None
        
        if net_debt is None:
            return None
        
        return net_debt / adj_ebitda
    
    def calculate_ev(
        self, 
        adj_ebitda: Optional[float], 
        ebitda_multiple: Optional[float]
    ) -> Optional[float]:
        """
        EV（企業価値）を計算
        
        Args:
            adj_ebitda: 調整後EBITDA
            ebitda_multiple: EBITDA倍率
        
        Returns:
            EV（未入力の場合はNone）
        """
        if adj_ebitda is None or ebitda_multiple is None:
            return None
        
        return adj_ebitda * ebitda_multiple
    
    def calculate_equity_value(
        self, 
        ev: Optional[float], 
        net_debt: Optional[float]
    ) -> Optional[float]:
        """
        Equity Value（株主価値）を計算
        
        Args:
            ev: 企業価値（EV）
            net_debt: Net Debt
        
        Returns:
            Equity Value（evがNoneの場合はNone）
        """
        if ev is None:
            return None
        
        if net_debt is None:
            net_debt = 0.0
        
        return ev - net_debt
    
    def calculate_qualitative_total(
        self,
        fit_score: Optional[int],
        brand_score: Optional[int],
        digital_score: Optional[int],
        scarcity_score: Optional[int]
    ) -> int:
        """
        定性合計を計算
        
        Args:
            fit_score: 領域・業態適合度（1〜5点）
            brand_score: ブランド・独自性（1〜5点）
            digital_score: ファンベース・D2C（1〜5点）
            scarcity_score: 特定分野・地域性（1〜5点）
        
        Returns:
            定性合計スコア（4〜20点、未入力は0として扱う）
        """
        total = 0
        
        if fit_score is not None:
            total += fit_score
        if brand_score is not None:
            total += brand_score
        if digital_score is not None:
            total += digital_score
        if scarcity_score is not None:
            total += scarcity_score
        
        return total
    
    # ========== 2) 定量（財務）の離散判定 ==========
    
    def rate_sales(self, sales: Optional[float]) -> Rating:
        """
        売上高判定
        
        Args:
            sales: 売上高（百万円単位）
        
        Returns:
            判定結果（〇/△/×）
        """
        if sales is None:
            return Rating.NO_DATA
        
        if sales >= 500:
            return Rating.GOOD  # 〇
        elif sales >= 300:
            return Rating.WARNING  # △
        else:
            return Rating.FAIL  # ×
    
    def rate_adj_ebitda(self, adj_ebitda: Optional[float]) -> Rating:
        """
        調整後EBITDA判定
        
        Args:
            adj_ebitda: 調整後EBITDA（百万円単位）
        
        Returns:
            判定結果（◎/〇/×）
        """
        if adj_ebitda is None:
            return Rating.NO_DATA
        
        if adj_ebitda >= 100:
            return Rating.EXCELLENT  # ◎
        elif adj_ebitda >= 50:
            return Rating.GOOD  # 〇
        else:
            return Rating.FAIL  # ×
    
    def rate_nd_to_ebitda(self, nd_to_ebitda: Optional[float]) -> Rating:
        """
        ND/EBITDA判定
        
        Args:
            nd_to_ebitda: ND/EBITDA倍率
        
        Returns:
            判定結果（◎/〇/×/数値未入力）
        """
        if nd_to_ebitda is None:
            return Rating.NO_DATA
        
        if nd_to_ebitda <= 3:
            return Rating.EXCELLENT  # ◎
        elif nd_to_ebitda <= 4:
            return Rating.GOOD  # 〇
        else:
            return Rating.FAIL  # ×
    
    def rate_ebitda_multiple(self, ebitda_multiple: Optional[float]) -> Rating:
        """
        EBITDA倍率判定
        
        Args:
            ebitda_multiple: EBITDA倍率
        
        Returns:
            判定結果（◎/〇/×/数値未入力）
        """
        if ebitda_multiple is None:
            return Rating.NO_DATA
        
        if ebitda_multiple <= 3:
            return Rating.EXCELLENT  # ◎
        elif ebitda_multiple <= 4:
            return Rating.GOOD  # 〇
        else:
            return Rating.FAIL  # ×
    
    def rate_ev(self, ev: Optional[float]) -> Rating:
        """
        EV判定（参考：サイズ適合）
        
        注：EVは×判定を持たない（ゲート要因にしない）
        
        Args:
            ev: 企業価値（百万円単位）
        
        Returns:
            判定結果（〇/△/（空欄））
        """
        if ev is None:
            return Rating.EMPTY
        
        if 1000 <= ev <= 2500:
            return Rating.GOOD  # 〇
        else:
            return Rating.WARNING  # △
    
    def rate_equity_value(self, equity_value: Optional[float]) -> Rating:
        """
        Equity Value判定（参考：サイズ適合）
        
        注：Equity Valueは×判定を持たない（ゲート要因にしない）
        
        Args:
            equity_value: 株主価値（百万円単位）
        
        Returns:
            判定結果（〇/△/数値未入力）
        """
        if equity_value is None:
            return Rating.NO_DATA
        
        if 300 <= equity_value <= 1500:
            return Rating.GOOD  # 〇
        else:
            return Rating.WARNING  # △
    
    # ========== 3) 定量総合判定（Quant Gate） ==========
    
    def evaluate_quantitative_gate(
        self,
        sales_rating: Rating,
        adj_ebitda_rating: Rating,
        nd_to_ebitda_rating: Rating,
        ebitda_multiple_rating: Rating
    ) -> GateResult:
        """
        定量総合判定（Quant Gate）
        
        定量判定の対象範囲に×が1つでもある場合NG、なければOK
        
        Args:
            sales_rating: 売上高判定
            adj_ebitda_rating: 調整後EBITDA判定
            nd_to_ebitda_rating: ND/EBITDA判定
            ebitda_multiple_rating: EBITDA倍率判定
        
        Returns:
            ゲート判定結果（OK/NG）
        """
        # ×が1つでもあればNG
        ratings = [
            sales_rating,
            adj_ebitda_rating,
            nd_to_ebitda_rating,
            ebitda_multiple_rating
        ]
        
        if any(rating == Rating.FAIL for rating in ratings):
            return GateResult.NG
        
        return GateResult.OK
    
    # ========== 4) 定性判定（Qual Gate） ==========
    
    def evaluate_qualitative_gate(self, qual_total: int) -> bool:
        """
        定性判定（Qual Gate）
        
        Args:
            qual_total: 定性合計スコア（4〜20点）
        
        Returns:
            True: 合格（15点以上）
            False: 不合格（15点未満）
        """
        return qual_total >= 15
    
    # ========== 5) 最終判定 ==========
    
    def make_final_decision(
        self,
        quant_result: GateResult,
        qual_passed: bool
    ) -> FinalDecision:
        """
        最終判定（見送り/見送りでない）
        
        Args:
            quant_result: 定量ゲート判定結果
            qual_passed: 定性ゲート合格フラグ
        
        Returns:
            最終判定（見送り/見送りでない）
        """
        # 見送り条件: (quant_result == NG) OR (qual_total < 15)
        if quant_result == GateResult.NG or not qual_passed:
            return FinalDecision.SKIP
        
        # 見送りでない条件: (quant_result == OK) AND (qual_total >= 15)
        return FinalDecision.PASS
    
    # ========== 統合計算メソッド ==========
    
    def calculate_all(
        self,
        # 入力変数（定量）
        sales: Optional[float],
        adj_ebitda: Optional[float],
        net_debt: Optional[float],
        ebitda_multiple: Optional[float],
        # 入力変数（定性）
        fit_score: Optional[int],
        brand_score: Optional[int],
        digital_score: Optional[int],
        scarcity_score: Optional[int]
    ) -> Dict:
        """
        全計算を一括実行
        
        Args:
            sales: 売上高（百万円）
            adj_ebitda: 調整後EBITDA（百万円）
            net_debt: Net Debt（百万円）
            ebitda_multiple: EBITDA倍率
            fit_score: 領域・業態適合度（1〜5点）
            brand_score: ブランド・独自性（1〜5点）
            digital_score: ファンベース・D2C（1〜5点）
            scarcity_score: 特定分野・地域性（1〜5点）
        
        Returns:
            計算結果の辞書
        """
        # 1) 中間計算
        nd_to_ebitda = self.calculate_nd_to_ebitda(net_debt, adj_ebitda)
        ev = self.calculate_ev(adj_ebitda, ebitda_multiple)
        equity_value = self.calculate_equity_value(ev, net_debt)
        qual_total = self.calculate_qualitative_total(
            fit_score, brand_score, digital_score, scarcity_score
        )
        
        # 2) 定量判定
        sales_rating = self.rate_sales(sales)
        adj_ebitda_rating = self.rate_adj_ebitda(adj_ebitda)
        nd_to_ebitda_rating = self.rate_nd_to_ebitda(nd_to_ebitda)
        ebitda_multiple_rating = self.rate_ebitda_multiple(ebitda_multiple)
        ev_rating = self.rate_ev(ev)
        equity_value_rating = self.rate_equity_value(equity_value)
        
        # 3) 定量総合判定
        quant_result = self.evaluate_quantitative_gate(
            sales_rating,
            adj_ebitda_rating,
            nd_to_ebitda_rating,
            ebitda_multiple_rating
        )
        
        # 4) 定性判定
        qual_passed = self.evaluate_qualitative_gate(qual_total)
        
        # 5) 最終判定
        final_decision = self.make_final_decision(quant_result, qual_passed)
        
        # 結果をまとめる
        return {
            # 中間計算結果
            'derived_metrics': {
                'nd_to_ebitda': nd_to_ebitda,
                'ev': ev,
                'equity_value': equity_value,
                'qualitative_total': qual_total
            },
            # 定量判定結果
            'quantitative_ratings': {
                'sales': sales_rating.value,
                'adj_ebitda': adj_ebitda_rating.value,
                'nd_to_ebitda': nd_to_ebitda_rating.value,
                'ebitda_multiple': ebitda_multiple_rating.value,
                'ev': ev_rating.value,  # 参考（ゲート要因ではない）
                'equity_value': equity_value_rating.value  # 参考（ゲート要因ではない）
            },
            # ゲート判定結果
            'gate_results': {
                'quantitative': quant_result.value,
                'qualitative': '合格' if qual_passed else '不合格'
            },
            # 最終判定
            'final_decision': final_decision.value,
            # 判定理由
            'reasoning': {
                'quantitative_ng_reasons': self._get_quant_ng_reasons(
                    sales_rating,
                    adj_ebitda_rating,
                    nd_to_ebitda_rating,
                    ebitda_multiple_rating
                ),
                'qualitative_score': qual_total,
                'qualitative_threshold': 15
            }
        }
    
    def _get_quant_ng_reasons(
        self,
        sales_rating: Rating,
        adj_ebitda_rating: Rating,
        nd_to_ebitda_rating: Rating,
        ebitda_multiple_rating: Rating
    ) -> List[str]:
        """
        定量NGの理由を取得
        
        Args:
            各判定結果
        
        Returns:
            NG理由のリスト
        """
        reasons = []
        
        if sales_rating == Rating.FAIL:
            reasons.append('売上高が300百万円未満')
        if adj_ebitda_rating == Rating.FAIL:
            reasons.append('調整後EBITDAが50百万円未満')
        if nd_to_ebitda_rating == Rating.FAIL:
            reasons.append('ND/EBITDA倍率が4倍超')
        if ebitda_multiple_rating == Rating.FAIL:
            reasons.append('EBITDA倍率が4倍超')
        
        return reasons

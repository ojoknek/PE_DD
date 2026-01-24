"""
統合ワークフローモジュール

案件ディレクトリをスキャンし、NN DDとIM DDのワークフローを自動実行します。
"""
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from dd_logic.nn_dd.workflows.nn_dd_workflow import run_nn_dd_workflow
from dd_logic.im_dd.workflows.im_dd_workflow import run_im_dd_workflow

logger = logging.getLogger(__name__)


class DealProcessor:
    """案件処理クラス"""
    
    def __init__(self, deal_dir: str):
        """
        DealProcessorを初期化
        
        Args:
            deal_dir: 案件ディレクトリのパス（deals/[deal_name]）
        """
        self.deal_dir = Path(deal_dir)
        if not self.deal_dir.exists():
            raise ValueError(f"案件ディレクトリが存在しません: {deal_dir}")
    
    def process_all(self) -> Dict[str, Any]:
        """
        全てのDDワークフローを実行（NN DD + IM DD）
        
        Returns:
            処理結果の辞書
        """
        logger.info(f"案件処理開始: {self.deal_dir}")
        
        results = {
            "deal_name": self.deal_dir.name,
            "nn_dd": None,
            "im_dd": None,
            "status": "success"
        }
        
        # NN DDを実行
        try:
            logger.info("NN DDワークフローを実行中...")
            nn_result = run_nn_dd_workflow(str(self.deal_dir))
            results["nn_dd"] = nn_result
            if nn_result.get("status") != "success":
                results["status"] = "partial_success"
        except Exception as e:
            logger.error(f"NN DDワークフローエラー: {e}")
            results["nn_dd"] = {"status": "error", "message": str(e)}
            results["status"] = "partial_success"
        
        # IM DDを実行
        try:
            logger.info("IM DDワークフローを実行中...")
            im_result = run_im_dd_workflow(str(self.deal_dir))
            results["im_dd"] = im_result
            if im_result.get("status") != "success":
                results["status"] = "partial_success"
        except Exception as e:
            logger.error(f"IM DDワークフローエラー: {e}")
            results["im_dd"] = {"status": "error", "message": str(e)}
            results["status"] = "partial_success"
        
        logger.info(f"案件処理完了: {self.deal_dir}")
        return results
    
    def process_nn_only(self) -> Dict[str, Any]:
        """
        NN DDのみを実行
        
        Returns:
            処理結果の辞書
        """
        logger.info(f"NN DDのみ実行: {self.deal_dir}")
        
        try:
            result = run_nn_dd_workflow(str(self.deal_dir))
            return {
                "deal_name": self.deal_dir.name,
                "nn_dd": result,
                "status": result.get("status", "success")
            }
        except Exception as e:
            logger.error(f"NN DDワークフローエラー: {e}")
            return {
                "deal_name": self.deal_dir.name,
                "nn_dd": {"status": "error", "message": str(e)},
                "status": "error"
            }
    
    def process_im_only(self) -> Dict[str, Any]:
        """
        IM DDのみを実行
        
        Returns:
            処理結果の辞書
        """
        logger.info(f"IM DDのみ実行: {self.deal_dir}")
        
        try:
            result = run_im_dd_workflow(str(self.deal_dir))
            return {
                "deal_name": self.deal_dir.name,
                "im_dd": result,
                "status": result.get("status", "success")
            }
        except Exception as e:
            logger.error(f"IM DDワークフローエラー: {e}")
            return {
                "deal_name": self.deal_dir.name,
                "im_dd": {"status": "error", "message": str(e)},
                "status": "error"
            }
    
    def scan_deal_directory(self) -> Dict[str, Any]:
        """
        案件ディレクトリをスキャンして情報を取得
        
        Returns:
            スキャン結果の辞書
        """
        scan_result = {
            "deal_name": self.deal_dir.name,
            "nn_files": [],
            "im_files": [],
            "has_nn": False,
            "has_im": False
        }
        
        # NNディレクトリをスキャン
        nn_dir = self.deal_dir / "nn"
        if nn_dir.exists():
            pdf_files = list(nn_dir.glob("**/*.pdf"))
            md_files = list(nn_dir.glob("**/*.md"))
            scan_result["nn_files"] = [str(f) for f in pdf_files + md_files]
            scan_result["has_nn"] = len(scan_result["nn_files"]) > 0
        
        # IMディレクトリをスキャン
        im_dir = self.deal_dir / "im"
        if im_dir.exists():
            pdf_files = list(im_dir.glob("**/*.pdf"))
            scan_result["im_files"] = [str(f) for f in pdf_files]
            scan_result["has_im"] = len(scan_result["im_files"]) > 0
        
        return scan_result


def process_deal(deal_dir: str, process_type: str = "all") -> Dict[str, Any]:
    """
    案件を処理する簡易関数
    
    Args:
        deal_dir: 案件ディレクトリのパス
        process_type: 処理タイプ（"all", "nn", "im"）
    
    Returns:
        処理結果の辞書
    """
    processor = DealProcessor(deal_dir)
    
    if process_type == "nn":
        return processor.process_nn_only()
    elif process_type == "im":
        return processor.process_im_only()
    else:
        return processor.process_all()

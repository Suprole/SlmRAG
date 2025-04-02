"""
ロガーモジュール

アプリケーション全体で使用できる汎用的なロギング機能を提供します。
コンソールへの出力とファイルへの書き込みの両方をサポートします。
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional, Union, Dict, Any, List

class Logger:
    """
    汎用的なロガークラス
    
    異なるログレベルと出力先（コンソール、ファイル）をサポートします。
    アプリケーション全体で一貫したロギングを提供します。
    """
    
    # ログレベル定数
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    
    # シングルトンインスタンス
    _instances: Dict[str, 'Logger'] = {}
    
    def __new__(cls, name: str = "app", *args, **kwargs):
        """
        シングルトンパターンを実装してロガーの再利用を保証
        
        Args:
            name: ロガーの名前
        """
        if name not in cls._instances:
            cls._instances[name] = super(Logger, cls).__new__(cls)
        return cls._instances[name]
    
    def __init__(
        self, 
        name: str = "app", 
        level: int = logging.INFO,
        console_output: bool = True,
        file_output: bool = False, 
        log_dir: str = "logs",
        format_string: str = "%(asctime)s [%(levelname)s] %(message)s"
    ):
        """
        ロガーを初期化
        
        Args:
            name: ロガーの名前
            level: ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
            console_output: コンソールに出力するかどうか
            file_output: ファイルに出力するかどうか
            log_dir: ログファイルを格納するディレクトリ
            format_string: ログメッセージのフォーマット
        """
        # 既に初期化されている場合は処理をスキップ
        if hasattr(self, 'logger'):
            return
            
        self.name = name
        self.level = level
        self.console_output = console_output
        self.file_output = file_output
        self.log_dir = log_dir
        self.format_string = format_string
        
        # ロガーを設定
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.handlers = []  # ハンドラを初期化
        
        # フォーマッタを作成
        formatter = logging.Formatter(format_string)
        
        # コンソール出力
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
        # ファイル出力
        if file_output:
            try:
                # ログディレクトリが存在しない場合は作成
                os.makedirs(log_dir, exist_ok=True)
                
                # 日付を含むログファイル名を作成
                date_str = datetime.now().strftime("%Y-%m-%d")
                log_file = os.path.join(log_dir, f"{name}_{date_str}.log")
                
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                # ファイルハンドラの作成に失敗した場合は警告を出力
                print(f"ログファイルの作成に失敗しました: {e}")
    
    def update_config(
        self, 
        level: Optional[int] = None,
        console_output: Optional[bool] = None,
        file_output: Optional[bool] = None
    ) -> None:
        """
        ロガーの設定を更新
        
        Args:
            level: 新しいログレベル（指定された場合）
            console_output: コンソール出力の有無（指定された場合）
            file_output: ファイル出力の有無（指定された場合）
        """
        # ログレベルの更新
        if level is not None:
            self.level = level
            self.logger.setLevel(level)
            
        # ハンドラの更新が必要な場合
        if console_output is not None or file_output is not None:
            # 現在の設定を保存
            if console_output is not None:
                self.console_output = console_output
            if file_output is not None:
                self.file_output = file_output
                
            # ハンドラをリセット
            self.logger.handlers = []
            
            # 設定を再適用
            formatter = logging.Formatter(self.format_string)
            
            # コンソール出力
            if self.console_output:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)
                
            # ファイル出力
            if self.file_output:
                try:
                    os.makedirs(self.log_dir, exist_ok=True)
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    log_file = os.path.join(self.log_dir, f"{self.name}_{date_str}.log")
                    
                    file_handler = logging.FileHandler(log_file, encoding='utf-8')
                    file_handler.setFormatter(formatter)
                    self.logger.addHandler(file_handler)
                except Exception as e:
                    print(f"ログファイルの作成に失敗しました: {e}")
    
    def debug(self, message: Any, *args, **kwargs) -> None:
        """DEBUGレベルのログを記録"""
        self.logger.debug(message, *args, **kwargs)
        
    def info(self, message: Any, *args, **kwargs) -> None:
        """INFOレベルのログを記録"""
        self.logger.info(message, *args, **kwargs)
        
    def warning(self, message: Any, *args, **kwargs) -> None:
        """WARNINGレベルのログを記録"""
        self.logger.warning(message, *args, **kwargs)
        
    def error(self, message: Any, *args, **kwargs) -> None:
        """ERRORレベルのログを記録"""
        self.logger.error(message, *args, **kwargs)
        
    def critical(self, message: Any, *args, **kwargs) -> None:
        """CRITICALレベルのログを記録"""
        self.logger.critical(message, *args, **kwargs)
        
    def exception(self, message: Any, *args, exc_info: bool = True, **kwargs) -> None:
        """例外情報を含むERRORレベルのログを記録"""
        self.logger.exception(message, *args, exc_info=exc_info, **kwargs)
        
    def log_dict(self, data: Dict[str, Any], level: int = logging.INFO) -> None:
        """
        辞書データをログに記録
        
        Args:
            data: ログに記録する辞書データ
            level: ログレベル
        """
        for key, value in data.items():
            self.logger.log(level, f"{key}: {value}")
            
    def log_api_request(
        self, 
        method: str, 
        endpoint: str, 
        status_code: int, 
        response_time: float, 
        user_id: Optional[str] = None
    ) -> None:
        """
        API呼び出しのログを記録
        
        Args:
            method: HTTPメソッド（GET, POST, etc）
            endpoint: 呼び出されたエンドポイント
            status_code: レスポンスステータスコード
            response_time: レスポンス時間（秒）
            user_id: ユーザーID（オプション）
        """
        user_info = f" [user: {user_id}]" if user_id else ""
        self.info(f"API {method} {endpoint} - Status: {status_code}, Time: {response_time:.4f}s{user_info}")
            
    def get_underlying_logger(self) -> logging.Logger:
        """基礎となるロガーオブジェクトを取得"""
        return self.logger


# 使いやすいようにデフォルトロガーのインスタンスを作成
default_logger = Logger(name="ragchat")

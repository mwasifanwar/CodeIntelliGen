import os
from typing import Dict, Any

class Settings:
    def __init__(self):
        self.API_HOST = os.getenv("CODE_INTELLIGEN_HOST", "0.0.0.0")
        self.API_PORT = int(os.getenv("CODE_INTELLIGEN_PORT", "8000"))
        self.DEBUG = os.getenv("CODE_INTELLIGEN_DEBUG", "False").lower() == "true"
        
        self.MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", "./model_cache")
        self.MAX_CODE_LENGTH = int(os.getenv("MAX_CODE_LENGTH", "1000"))
        self.DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
        
        self.SUPPORTED_LANGUAGES = [
            "python", "javascript", "java", "cpp", "c", "csharp", 
            "php", "ruby", "go", "rust", "typescript"
        ]
        
        self.SECURITY_SCAN_ENABLED = os.getenv("SECURITY_SCAN_ENABLED", "True").lower() == "true"
        self.AUTO_TEST_GENERATION = os.getenv("AUTO_TEST_GENERATION", "True").lower() == "true"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'API_HOST': self.API_HOST,
            'API_PORT': self.API_PORT,
            'DEBUG': self.DEBUG,
            'MODEL_CACHE_DIR': self.MODEL_CACHE_DIR,
            'MAX_CODE_LENGTH': self.MAX_CODE_LENGTH,
            'DEFAULT_TEMPERATURE': self.DEFAULT_TEMPERATURE,
            'SUPPORTED_LANGUAGES': self.SUPPORTED_LANGUAGES,
            'SECURITY_SCAN_ENABLED': self.SECURITY_SCAN_ENABLED,
            'AUTO_TEST_GENERATION': self.AUTO_TEST_GENERATION
        }
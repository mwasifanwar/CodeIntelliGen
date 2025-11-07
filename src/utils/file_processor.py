import os
import ast
import hashlib
from typing import List, Dict, Any

class FileProcessor:
    def __init__(self):
        self.supported_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust'
        }
    
    def read_file(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}")
    
    def write_file(self, file_path: str, content: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    
    def get_file_language(self, file_path: str) -> str:
        _, ext = os.path.splitext(file_path)
        return self.supported_extensions.get(ext.lower(), 'unknown')
    
    def scan_directory(self, directory: str) -> List[Dict[str, Any]]:
        files_info = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                language = self.get_file_language(file_path)
                
                if language != 'unknown':
                    try:
                        content = self.read_file(file_path)
                        files_info.append({
                            'path': file_path,
                            'language': language,
                            'size': len(content),
                            'lines': content.count('\n') + 1,
                            'hash': hashlib.md5(content.encode()).hexdigest()
                        })
                    except:
                        continue
        
        return files_info
    
    def validate_code_syntax(self, code: str, language: str) -> bool:
        if language == 'python':
            try:
                ast.parse(code)
                return True
            except SyntaxError:
                return False
        return True
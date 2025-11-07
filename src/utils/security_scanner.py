import re
import ast
from typing import List, Dict, Any

class SecurityScanner:
    def __init__(self):
        self.vulnerability_patterns = {
            'sql_injection': [
                r"execute\(.*\+.*\)",
                r"executemany\(.*\+.*\)",
                r"cursor\.execute\(f\".*\"\)",
                r"db\.execute\(.*\+.*\)"
            ],
            'xss_vulnerability': [
                r"innerHTML.*=.*\+",
                r"document\.write\(.*\+\)",
                r"eval\(.*\)"
            ],
            'path_traversal': [
                r"open\(.*\+.*\)",
                r"file\(.*\+.*\)",
                r"readfile\(.*\+.*\)"
            ],
            'hardcoded_secrets': [
                r"password\s*=\s*['\"][^'\"]+['\"]",
                r"api_key\s*=\s*['\"][^'\"]+['\"]",
                r"secret\s*=\s*['\"][^'\"]+['\"]"
            ]
        }
    
    def scan_code(self, code: str, language: str = "python") -> List[Dict[str, Any]]:
        vulnerabilities = []
        
        vulnerabilities.extend(self._pattern_scan(code))
        vulnerabilities.extend(self._ast_analysis(code, language))
        vulnerabilities.extend(self._hardcoded_secrets_scan(code))
        
        return vulnerabilities
    
    def _pattern_scan(self, code: str) -> List[Dict[str, Any]]:
        issues = []
        
        for vuln_type, patterns in self.vulnerability_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)
                for match in matches:
                    issues.append({
                        'type': 'security',
                        'category': vuln_type,
                        'severity': 'high',
                        'message': f'Potential {vuln_type.replace("_", " ")} detected',
                        'line': code[:match.start()].count('\n') + 1,
                        'snippet': match.group()
                    })
        
        return issues
    
    def _ast_analysis(self, code: str, language: str) -> List[Dict[str, Any]]:
        issues = []
        
        if language == "python":
            try:
                tree = ast.parse(code)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name):
                            if node.func.id in ['eval', 'exec', 'compile']:
                                issues.append({
                                    'type': 'security',
                                    'category': 'code_injection',
                                    'severity': 'high',
                                    'message': f'Use of dangerous function: {node.func.id}',
                                    'line': getattr(node, 'lineno', 'unknown')
                                })
                    
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name in ['pickle', 'marshal']:
                                issues.append({
                                    'type': 'security',
                                    'category': 'unsafe_deserialization',
                                    'severity': 'medium',
                                    'message': f'Use of potentially unsafe module: {alias.name}',
                                    'line': getattr(node, 'lineno', 'unknown')
                                })
            
            except SyntaxError:
                pass
        
        return issues
    
    def _hardcoded_secrets_scan(self, code: str) -> List[Dict[str, Any]]:
        issues = []
        
        secret_patterns = {
            'password': r"password\s*=\s*['\"]([^'\"]+)['\"]",
            'api_key': r"api[_-]?key\s*=\s*['\"]([^'\"]+)['\"]",
            'secret': r"secret\s*=\s*['\"]([^'\"]+)['\"]",
            'token': r"token\s*=\s*['\"]([^'\"]+)['\"]"
        }
        
        for secret_type, pattern in secret_patterns.items():
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                issues.append({
                    'type': 'security',
                    'category': 'hardcoded_secret',
                    'severity': 'high',
                    'message': f'Potential hardcoded {secret_type} detected',
                    'line': code[:match.start()].count('\n') + 1,
                    'snippet': match.group()
                })
        
        return issues
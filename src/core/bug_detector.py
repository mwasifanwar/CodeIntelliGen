import ast
import re
from typing import List, Dict, Any
import subprocess
import tempfile
import os

class BugDetector:
    def __init__(self):
        self.patterns = {
            'sql_injection': [
                r"execute\(.*\+.*\)",
                r"executemany\(.*\+.*\)",
                r"cursor\.execute\(f\".*\"\)"
            ],
            'xss': [
                r"innerHTML.*=.*\+",
                r"document\.write\(.*\+\)"
            ],
            'buffer_overflow': [
                r"strcpy\(",
                r"strcat\(",
                r"gets\("
            ],
            'memory_leak': [
                r"malloc\(.*\).*;.*[^free]",
                r"new.*[^delete]"
            ]
        }
    
    def detect_vulnerabilities(self, code: str, language: str = "python") -> List[Dict[str, Any]]:
        issues = []
        
        if language == "python":
            issues.extend(self._analyze_python_code(code))
        
        issues.extend(self._pattern_match(code))
        issues.extend(self._static_analysis(code))
        
        return issues
    
    def _analyze_python_code(self, code: str) -> List[Dict[str, Any]]:
        issues = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id == 'eval':
                            issues.append({
                                'type': 'security',
                                'severity': 'high',
                                'message': 'Use of eval() function detected',
                                'line': node.lineno if hasattr(node, 'lineno') else 'unknown'
                            })
                        elif node.func.id == 'exec':
                            issues.append({
                                'type': 'security',
                                'severity': 'high',
                                'message': 'Use of exec() function detected',
                                'line': node.lineno if hasattr(node, 'lineno') else 'unknown'
                            })
                
                elif isinstance(node, ast.Try):
                    if not node.handlers:
                        issues.append({
                            'type': 'error_handling',
                            'severity': 'medium',
                            'message': 'Empty try block without exception handling',
                            'line': node.lineno if hasattr(node, 'lineno') else 'unknown'
                        })
        
        except SyntaxError as e:
            issues.append({
                'type': 'syntax',
                'severity': 'high',
                'message': f'Syntax error: {str(e)}',
                'line': e.lineno
            })
        
        return issues
    
    def _pattern_match(self, code: str) -> List[Dict[str, Any]]:
        issues = []
        
        for vuln_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code)
                for match in matches:
                    issues.append({
                        'type': 'security',
                        'severity': 'high',
                        'message': f'Potential {vuln_type.replace("_", " ")} detected',
                        'line': self._get_line_number(code, match.start()),
                        'pattern': pattern
                    })
        
        return issues
    
    def _static_analysis(self, code: str) -> List[Dict[str, Any]]:
        issues = []
        
        if "password" in code and "encrypt" not in code:
            issues.append({
                'type': 'security',
                'severity': 'medium',
                'message': 'Potential plain text password storage'
            })
        
        if "TODO" in code or "FIXME" in code:
            issues.append({
                'type': 'maintenance',
                'severity': 'low',
                'message': 'TODO/FIXME comment found'
            })
        
        return issues
    
    def _get_line_number(self, code: str, position: int) -> int:
        return code[:position].count('\n') + 1
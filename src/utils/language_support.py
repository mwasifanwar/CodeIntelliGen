from typing import Dict, List, Any

class LanguageSupport:
    def __init__(self):
        self.language_templates = {
            'python': {
                'function': 'def {function_name}({parameters}):\n    {body}',
                'class': 'class {class_name}:\n    {body}',
                'import': 'import {module}',
                'comment': '# {comment}'
            },
            'javascript': {
                'function': 'function {function_name}({parameters}) {{\n    {body}\n}}',
                'class': 'class {class_name} {{\n    {body}\n}}',
                'import': 'const {module} = require(\"{package}\");',
                'comment': '// {comment}'
            },
            'java': {
                'function': 'public {return_type} {function_name}({parameters}) {{\n    {body}\n}}',
                'class': 'public class {class_name} {{\n    {body}\n}}',
                'import': 'import {package}.{module};',
                'comment': '// {comment}'
            }
        }
        
        self.language_configs = {
            'python': {
                'extension': '.py',
                'single_line_comment': '#',
                'multi_line_comment': ('"""', '"""')
            },
            'javascript': {
                'extension': '.js',
                'single_line_comment': '//',
                'multi_line_comment': ('/*', '*/')
            },
            'java': {
                'extension': '.java',
                'single_line_comment': '//',
                'multi_line_comment': ('/*', '*/')
            }
        }
    
    def get_template(self, language: str, template_type: str) -> str:
        return self.language_templates.get(language, {}).get(template_type, '')
    
    def get_language_config(self, language: str) -> Dict[str, Any]:
        return self.language_configs.get(language, {})
    
    def generate_function(self, language: str, function_name: str, parameters: str, body: str, return_type: str = 'void') -> str:
        template = self.get_template(language, 'function')
        
        if language == 'java':
            return template.format(
                return_type=return_type,
                function_name=function_name,
                parameters=parameters,
                body=body
            )
        else:
            return template.format(
                function_name=function_name,
                parameters=parameters,
                body=body
            )
    
    def supported_languages(self) -> List[str]:
        return list(self.language_templates.keys())
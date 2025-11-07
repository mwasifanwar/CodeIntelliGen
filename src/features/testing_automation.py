import ast
import re
from typing import List, Dict, Any
from ..core.code_generator import CodeGenerator

class TestGenerator:
    def __init__(self, model_path: str = None):
        self.generator = CodeGenerator(model_path)
    
    def generate_unit_tests(self, code: str, language: str = "python") -> str:
        if language == "python":
            return self._generate_python_tests(code)
        else:
            return self._generate_generic_tests(code, language)
    
    def _generate_python_tests(self, code: str) -> str:
        functions = self._extract_functions(code)
        test_code = "import unittest\nimport sys\nimport os\n\n\nclass TestGeneratedCode(unittest.TestCase):\n"
        
        for func_name in functions:
            test_method = f"    def test_{func_name}(self):\n"
            test_method += f"        # Test for function {func_name}\n"
            test_method += f"        self.skipTest('Test implementation needed for {func_name}')\n"
            test_method += f"        # Add your test logic here\n\n"
            test_code += test_method
        
        test_code += "\n\nif __name__ == '__main__':\n    unittest.main()"
        
        return test_code
    
    def _extract_functions(self, code: str) -> List[str]:
        functions = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
        except:
            pass
        
        return functions
    
    def _generate_generic_tests(self, code: str, language: str) -> str:
        prompt = f"Generate comprehensive unit tests in {language} for the following code:\n\n{code}\n\nTest code:"
        
        tests = self.generator.generate_code(prompt, max_length=500, temperature=0.2)
        return tests
    
    def generate_test_cases(self, function_signature: str, language: str = "python") -> List[Dict[str, Any]]:
        prompt = f"Generate test cases for this {language} function: {function_signature}\n\nTest cases should include input parameters and expected output."
        
        test_cases_response = self.generator.generate_code(prompt, max_length=300, temperature=0.3)
        
        test_cases = []
        lines = test_cases_response.split('\n')
        
        for line in lines:
            if "input" in line.lower() or "test" in line.lower():
                test_cases.append({
                    'description': line.strip(),
                    'input': 'TODO',
                    'expected_output': 'TODO'
                })
        
        return test_cases
    
    def analyze_test_coverage(self, code: str, tests: str) -> Dict[str, Any]:
        analysis = {
            'functions_covered': 0,
            'total_functions': 0,
            'coverage_percentage': 0,
            'missing_tests': []
        }
        
        code_functions = self._extract_functions(code)
        test_functions = self._extract_functions(tests)
        
        analysis['total_functions'] = len(code_functions)
        analysis['functions_covered'] = len([f for f in code_functions if f"test_{f}" in test_functions])
        
        if analysis['total_functions'] > 0:
            analysis['coverage_percentage'] = (analysis['functions_covered'] / analysis['total_functions']) * 100
        
        analysis['missing_tests'] = [f for f in code_functions if f"test_{f}" not in test_functions]
        
        return analysis
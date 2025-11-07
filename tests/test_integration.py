import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.core.code_generator import CodeGenerator
from src.core.bug_detector import BugDetector
from src.features.code_completion import CodeCompleter

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.generator = CodeGenerator()
        self.detector = BugDetector()
        self.completer = CodeCompleter()
    
    def test_generate_and_analyze(self):
        prompt = "def calculate_factorial(n):"
        generated_code = self.generator.generate_code(prompt, max_length=100)
        
        issues = self.detector.detect_vulnerabilities(generated_code, "python")
        
        self.assertIsInstance(generated_code, str)
        self.assertIsInstance(issues, list)
    
    def test_complete_and_analyze(self):
        partial_code = "def process_data(data):"
        completions = self.completer.complete_line(partial_code)
        
        self.assertIsInstance(completions, list)
        self.assertGreater(len(completions), 0)

if __name__ == '__main__':
    unittest.main()
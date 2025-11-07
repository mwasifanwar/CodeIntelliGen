import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.core.code_generator import CodeGenerator

class TestCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = CodeGenerator()
    
    def test_generate_code_basic(self):
        prompt = "def hello_world():"
        result = self.generator.generate_code(prompt, max_length=50)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), len(prompt))
    
    def test_complete_function(self):
        function_sig = "def calculate_sum(a, b):"
        result = self.generator.complete_function(function_sig)
        self.assertIsInstance(result, str)
        self.assertIn("def calculate_sum", result)

if __name__ == '__main__':
    unittest.main()
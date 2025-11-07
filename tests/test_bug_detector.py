import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.core.bug_detector import BugDetector

class TestBugDetector(unittest.TestCase):
    def setUp(self):
        self.detector = BugDetector()
    
    def test_detect_vulnerabilities(self):
        test_code = """
        def insecure_function(user_input):
            import os
            os.system(user_input)
            return eval(user_input)
        """
        
        issues = self.detector.detect_vulnerabilities(test_code, "python")
        self.assertIsInstance(issues, list)
    
    def test_sql_injection_detection(self):
        test_code = "cursor.execute('SELECT * FROM users WHERE id = ' + user_input)"
        issues = self.detector.detect_vulnerabilities(test_code, "python")
        
        sql_injection_found = any(
            'sql injection' in issue['message'].lower() 
            for issue in issues
        )
        self.assertTrue(sql_injection_found)

if __name__ == '__main__':
    unittest.main()
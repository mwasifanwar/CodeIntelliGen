import argparse
import sys
import os

from src.core.code_generator import CodeGenerator
from src.core.bug_detector import BugDetector
from src.features.code_completion import CodeCompleter
from src.features.testing_automation import TestGenerator
from src.features.documentation_generator import DocumentationGenerator
from src.utils.file_processor import FileProcessor

def main():
    parser = argparse.ArgumentParser(description="CodeIntelliGen - AI-Powered Code Generation")
    
    parser.add_argument("--generate", type=str, help="Generate code from prompt")
    parser.add_argument("--detect-bugs", type=str, help="Detect bugs in code file")
    parser.add_argument("--complete", type=str, help="Complete partial code")
    parser.add_argument("--generate-tests", type=str, help="Generate tests for code file")
    parser.add_argument("--generate-docs", type=str, help="Generate documentation for code file")
    parser.add_argument("--language", type=str, default="python", help="Programming language")
    parser.add_argument("--output", type=str, help="Output file path")
    
    args = parser.parse_args()
    
    if args.generate:
        generator = CodeGenerator()
        generated_code = generator.generate_code(args.generate)
        print("Generated Code:")
        print(generated_code)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(generated_code)
            print(f"Code written to {args.output}")
    
    elif args.detect_bugs:
        processor = FileProcessor()
        detector = BugDetector()
        
        code = processor.read_file(args.detect_bugs)
        issues = detector.detect_vulnerabilities(code, args.language)
        
        print(f"Found {len(issues)} issues:")
        for issue in issues:
            print(f"- [{issue['severity'].upper()}] {issue['message']}")
    
    elif args.complete:
        completer = CodeCompleter()
        completions = completer.complete_line(args.complete, args.language)
        
        print("Code completions:")
        for i, completion in enumerate(completions, 1):
            print(f"{i}. {completion}")
    
    elif args.generate_tests:
        processor = FileProcessor()
        test_gen = TestGenerator()
        
        code = processor.read_file(args.generate_tests)
        tests = test_gen.generate_unit_tests(code, args.language)
        
        print("Generated Tests:")
        print(tests)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(tests)
            print(f"Tests written to {args.output}")
    
    elif args.generate_docs:
        processor = FileProcessor()
        doc_gen = DocumentationGenerator()
        
        code = processor.read_file(args.generate_docs)
        docs = doc_gen.generate_docstring(code, args.language)
        
        print("Generated Documentation:")
        print(docs)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(docs)
            print(f"Documentation written to {args.output}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
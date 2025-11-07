from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.code_generator import CodeGenerator
from src.core.bug_detector import BugDetector
from src.features.code_completion import CodeCompleter
from src.features.testing_automation import TestGenerator
from src.features.documentation_generator import DocumentationGenerator

api_router = APIRouter()

class CodeRequest(BaseModel):
    code: str
    language: str = "python"
    parameters: Dict[str, Any] = {}

class CompletionRequest(BaseModel):
    partial_code: str
    language: str = "python"

class TestRequest(BaseModel):
    code: str
    language: str = "python"
    test_framework: str = "unittest"

code_generator = CodeGenerator()
bug_detector = BugDetector()
code_completer = CodeCompleter()
test_generator = TestGenerator()
doc_generator = DocumentationGenerator()

@api_router.post("/generate-code")
async def generate_code(request: CodeRequest):
    try:
        generated_code = code_generator.generate_code(
            request.code,
            max_length=request.parameters.get('max_length', 100),
            temperature=request.parameters.get('temperature', 0.7)
        )
        return {"generated_code": generated_code, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/detect-bugs")
async def detect_bugs(request: CodeRequest):
    try:
        issues = bug_detector.detect_vulnerabilities(request.code, request.language)
        return {"issues": issues, "count": len(issues), "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/complete-code")
async def complete_code(request: CompletionRequest):
    try:
        completions = code_completer.complete_line(request.partial_code, request.language)
        return {"completions": completions, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/generate-tests")
async def generate_tests(request: TestRequest):
    try:
        tests = test_generator.generate_unit_tests(request.code, request.language)
        return {"tests": tests, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/generate-docs")
async def generate_docs(request: CodeRequest):
    try:
        documentation = doc_generator.generate_docstring(request.code, request.language)
        return {"documentation": documentation, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "CodeIntelliGen"}
SAMPLE_TEMPLATES = {
    "python_function": {
        "template": "def {function_name}({parameters}):\n    \"\"\"\n    {description}\n    \n    Args:\n        {args_doc}\n        \n    Returns:\n        {returns_doc}\n    \"\"\"\n    {body}",
        "variables": ["function_name", "parameters", "description", "args_doc", "returns_doc", "body"]
    },
    "python_class": {
        "template": "class {class_name}:\n    \"\"\"\n    {class_description}\n    \"\"\"\n    \n    def __init__(self{init_parameters}):\n        \"\"\"\n        Initialize {class_name}\n        \n        Args:\n            {init_args_doc}\n        \"\"\"\n        {init_body}",
        "variables": ["class_name", "class_description", "init_parameters", "init_args_doc", "init_body"]
    },
    "javascript_function": {
        "template": "/**\n * {description}\n * @param {params_doc}\n * @returns {returns_doc}\n */\nfunction {function_name}({parameters}) {{\n    {body}\n}}",
        "variables": ["function_name", "parameters", "description", "params_doc", "returns_doc", "body"]
    }
}

CODE_PATTERNS = {
    "python_imports": [
        "import {module}",
        "from {module} import {function}",
        "import {module} as {alias}"
    ],
    "python_boilerplate": [
        "#!/usr/bin/env python3",
        "# -*- coding: utf-8 -*-",
        "\"\"\"\n{module_description}\n\"\"\"",
        "__author__ = 'mwasifanwar'",
        "__version__ = '1.0.0'"
    ]
}
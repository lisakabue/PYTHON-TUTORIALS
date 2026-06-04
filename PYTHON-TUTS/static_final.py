#!/usr/bin/env python3
import os
import ast

# Starter Script for Automated Static Code Analysis Tool
# Scenario: You are a junior penetration tester at a manufacturing facility.
# Your mission is to identify vulnerabilities in the facility's software.

# Define vulnerability patterns
unsafe_functions = ["eval", "exec", "pickle.loads"]


def collect_source_files(directory, extension=".py"):
    """
    Recursively collects all source code files with a given extension
    from the specified directory.
    """
    source_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                source_files.append(os.path.join(root, file))
    return source_files


def parse_source_code(file_path):
    """
    Parses the source code file and returns its Abstract Syntax Tree (AST).
    """
    with open(file_path, "r", encoding="utf-8") as file:
        source = file.read()
    try:
        tree = ast.parse(source, filename=file_path)
        return tree
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
        return None


def is_vulnerable_function(node):
    """
    Checks if the function call node uses any unsafe functions.
    """
    if isinstance(node, ast.Call):
        func_name = ""

        if isinstance(node.func, ast.Name):
            func_name = node.func.id

        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                func_name = f"{node.func.value.id}.{node.func.attr}"
            else:
                func_name = node.func.attr

        if func_name in unsafe_functions:
            return True, func_name

    return False, None


def analyze_ast(tree, file_path):
    """
    Analyzes the AST of a source file for potential vulnerabilities.
    Returns a list of found issues.
    """
    issues = []
    for node in ast.walk(tree):
        vulnerable, func_name = is_vulnerable_function(node)
        if vulnerable:
            issue = {
                "file": file_path,
                "line": getattr(node, "lineno", "unknown"),
                "issue": f"Use of unsafe function '{func_name}'"
            }
            issues.append(issue)
    return issues


def main(directory):
    """
    Main function to perform static code analysis on all source files
    in the given directory.
    """
    all_issues = []
    source_files = collect_source_files(directory)

    for file in source_files:
        tree = parse_source_code(file)
        if tree:
            issues = analyze_ast(tree, file)
            all_issues.extend(issues)

    if all_issues:
        print("Vulnerabilities found:")
        for issue in all_issues:
            print(
                f"File: {issue['file']}, "
                f"Line: {issue['line']}, "
                f"Issue: {issue['issue']}"
            )
    else:
        print("No vulnerabilities found.")


if __name__ == "__main__":
    main(".")
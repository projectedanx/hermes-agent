import ast
import sys

def check_syntax(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        print(f"Syntax OK: {filepath}")
        return 0
    except SyntaxError as e:
        print(f"Syntax Error in {filepath}: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check_syntax("tinker-atropos/tinker_atropos/trainer.py"))

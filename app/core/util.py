import sys

def is_test_run():
    return "pytest" in sys.modules
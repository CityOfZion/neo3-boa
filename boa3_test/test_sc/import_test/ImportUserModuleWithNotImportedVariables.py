from boa3.sc.compiletime import public
from boa3_test.test_sc.variable_test.GlobalAssignmentBetweenFunctions import example


a = 15


@public
def main() -> int:
    return example()

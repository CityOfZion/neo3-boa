from boa3.builtin.compile_time import public
from boa3_test.test_sc.variable_test.GlobalAssignmentBetweenFunctions import example


a = 15


@public
def main() -> int:
    return example()

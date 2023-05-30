from boa3.builtin.compile_time import public
from boa3.builtin.type.helper import to_bytes, to_str


@public
def Main(condition: bool) -> str:
    result = "{["
    if condition:
        result = result + "]}"
    else:
        some_string = "value1|value2|value3"
        index = 0
        count = 0
        id_destiny = ""

        while index < len(some_string):
            c = some_string[index:index + 1]
            if to_str(to_bytes(c)) != "|":
                id_destiny = id_destiny + c
            else:
                if count > 0:
                    result = result + ","
                result = result + id_destiny
                id_destiny = ""
                count = count + 1
            index = index + 1
        if count > 0:
            result = result + ","
        result = result + id_destiny
        result = result + "]}"

    return result

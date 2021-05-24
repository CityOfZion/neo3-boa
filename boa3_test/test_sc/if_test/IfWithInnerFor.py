from boa3.builtin import public


@public
def Main(condition: bool) -> str:
    result = "{["
    if condition:
        result = result + "]}"
    else:
        some_string = "value1|value2|value3"
        count = 0
        id_destiny = ""

        for c in some_string:
            if c.to_bytes().to_str() != "|":
                id_destiny = id_destiny + c
            else:
                if count > 0:
                    result = result + ","
                result = result + id_destiny
                id_destiny = ""
                count = count + 1
        if count > 0:
            result = result + ","
        result = result + id_destiny
        result = result + "]}"

    return result

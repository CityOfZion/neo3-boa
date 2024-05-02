from boa3.builtin.compile_time import public


@public
def main(dict_: dict) -> str:
    match dict_:
        case {
            'ccccc': None,
            'ab': 'cd',
            '12': '34',
            'xy': 'zy',
            '00': '55',
        }:
            return "big dictionary"
        case {'key': 'value'}:
            return "key and value"
        case {}:
            return "empty dict"
        case _:
            return "default return"

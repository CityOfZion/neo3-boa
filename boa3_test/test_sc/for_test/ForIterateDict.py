def main() -> str:
    j = 20
    d = {
        'a': 1,
        'b': 4,
        4: 'blah',
        'm': j,
        'z': [1, 3, 4, 5, 'abcd', j]
    }

    output = ''
    for item in d.keys():
        output += item

    return output

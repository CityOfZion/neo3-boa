def main() -> bool:
    a = {'unit': 1, 'test': True}
    del a['unit']

    return a['test']

import ast


def get_auxiliary_name(node: ast.AST, aux_symbol_id: str) -> str:
    """
    Generates a name for auxiliary variables.

    :param node: the ast node that originates the auxiliary symbol
    :param aux_symbol_id: the id name of the auxiliary symbol
    :return: the unique name to the symbol.
    """
    return "{0}_{1}".format(aux_symbol_id, id(node))

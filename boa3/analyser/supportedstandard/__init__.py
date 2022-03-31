"""
Use Upper Kebab Case to name the standards in this dictionary
"""
from boa3.model.standards.nep11standard import Nep11Standard
from boa3.model.standards.nep17standard import Nep17Standard

neo_standards = {
    'NEP-11': Nep11Standard(),
    'NEP-17': Nep17Standard()
}

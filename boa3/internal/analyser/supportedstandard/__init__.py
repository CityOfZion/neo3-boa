"""
Use Upper Kebab Case to name the standards in this dictionary
"""
from boa3.internal.model.standards.nep11divisiblestandard import Nep11DivisibleStandard
from boa3.internal.model.standards.nep11nondivisiblestandard import Nep11NonDivisibleStandard
from boa3.internal.model.standards.nep17standard import Nep17Standard

neo_standards = {
    'NEP-11': [Nep11NonDivisibleStandard(), Nep11DivisibleStandard()],
    'NEP-17': [Nep17Standard()]
}

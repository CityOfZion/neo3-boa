__all__ = [
    'CodeOptimizer'
]

from boa3.internal.compiler.codegenerator.engine.executionscript import ExecutionScript
from boa3.internal.compiler.codegenerator.engine.neoengine import NeoEngine
from boa3.internal.compiler.codegenerator.optimizerhelper import OptimizationLevel
from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol


class CodeOptimizer:
    def __init__(self, symbol_table: dict[str, ISymbol]):
        if isinstance(symbol_table, dict):
            # works with a copy to prevent changes on the original symbol table
            symbol_table = symbol_table.copy()
        else:
            symbol_table = {}

        self.symbol_table = symbol_table
        self._map_instance = VMCodeMapping.instance()

    def optimize(self, optimization_level: OptimizationLevel = OptimizationLevel.DEFAULT):
        engine = NeoEngine()
        engine.load_script(ExecutionScript.from_code_map(self._map_instance))

        executed_instructions_addresses = set()

        # executed the methods to check if there are opcodes that are not executed
        for method in self.symbol_table.values():
            if isinstance(method, Method) and method.is_public:
                executed_instructions = engine.execute(method.start_address)

                executed_instructions_addresses.update(executed_instructions)

from typing import List, Dict, Optional

from boa3.internal.neo.vm.VMCode import VMCode


class VMCodeMap:
    def __init__(self):
        self._vm_code_list: List[VMCode] = []
        self._vm_code_addresses: List[int] = []

        # optimization so it's not needed to iterate over everything in search of targets
        self._vm_code_with_target: List[VMCode] = []

    def __len__(self) -> int:
        return self._vm_code_list.__len__()

    def clear(self):
        self._vm_code_addresses.clear()
        self._vm_code_list.clear()

    def get_code_map(self) -> Dict[int, VMCode]:
        size = len(self)
        return {self._vm_code_addresses[index]: self._vm_code_list[index] for index in range(size)}

    def get_code_list(self) -> List[VMCode]:
        return self._vm_code_list

    def get_code_with_target_list(self) -> List[VMCode]:
        return self._vm_code_with_target

    def get_bytecode_size(self) -> int:
        if len(self) < 1:
            return 0

        return self._vm_code_addresses[-1] + self._vm_code_list[-1].size

    def insert_code(self, vm_code: VMCode, has_target: bool = False):
        if vm_code not in self._vm_code_list:
            self._vm_code_addresses.append(self.get_bytecode_size())
            self._vm_code_list.append(vm_code)

            if has_target:
                self._vm_code_with_target.append(vm_code)

    def get_code(self, address: int) -> Optional[VMCode]:
        try:
            index = self._vm_code_addresses.index(address)
        except ValueError:
            # the address is not int the list
            if address >= self.get_bytecode_size():
                # the address is not in the bytecode
                return None

            # if the address is not the start of a instruction, gets the last instruction before given address
            code_address = 0
            for addr in self._vm_code_addresses:
                if addr > address:
                    break
                code_address = addr

            index = self._vm_code_addresses.index(code_address)

        return self._vm_code_list[index]

    def get_start_address(self, vm_code: VMCode) -> int:
        try:
            index = self._vm_code_list.index(vm_code)
            return self._vm_code_addresses[index]
        except ValueError:
            return 0

    def get_end_address(self, vm_code: VMCode) -> int:
        try:
            index = self._vm_code_list.index(vm_code) + 1
            if index == len(self._vm_code_list):
                return self.get_bytecode_size()
            else:
                return self._vm_code_addresses[index] - 1
        except ValueError:
            return 0

    def get_addresses(self, start_address: int, end_address: int) -> List[int]:
        if start_address > end_address:
            start_address, end_address = end_address, start_address

        addresses = []
        for address in range(start_address, end_address + 1):
            if address in self._vm_code_addresses:
                addresses.append(address)
        return addresses

    def get_addresses_from_codes(self, codes: List[VMCode]) -> List[int]:
        if len(codes) < 1:
            return []

        addresses = []
        for vm_code in codes:
            try:
                index = self._vm_code_list.index(vm_code)
                addresses.append(self._vm_code_addresses[index])
            except ValueError:
                continue

        return addresses

    def get_opcodes(self, addresses: List[int]) -> List[VMCode]:
        codes = []

        for address in sorted(addresses):
            try:
                index = self._vm_code_addresses.index(address)
                codes.append(self._vm_code_list[index])
            except ValueError:
                # address not in list
                continue

        return codes

    def update_addresses(self, start_address: int = 0):
        next_address = -1
        final_size = len(self._vm_code_list)

        if len(self._vm_code_addresses) > final_size:
            self._vm_code_addresses = self._vm_code_addresses[:final_size]

        for index in range(final_size):
            address = self._vm_code_addresses[index]

            if address >= start_address:
                if next_address < 0:
                    if index > 0:
                        new_address = self._vm_code_addresses[index - 1]
                        next_address = new_address + self._vm_code_list[index - 1].size
                    else:
                        next_address = 0

                if next_address != address:
                    if index < len(self._vm_code_addresses):
                        self._vm_code_addresses[index] = next_address
                    else:
                        self._vm_code_addresses.append(next_address)

                next_address += self._vm_code_list[index].size

    def move_to_end(self, first_code_address: int, last_code_address: int) -> Optional[int]:
        if last_code_address < first_code_address:
            return

        if (len(self._vm_code_addresses) > 0 and
                last_code_address == self._vm_code_addresses[-1]):
            # there's nothing to change if it's moving the all the codes
            return

        first_index = -1
        last_index = 0
        for index, address in enumerate(self._vm_code_addresses):
            if first_code_address <= address and first_index < 0:
                first_index = index
            elif address > last_code_address:
                last_index = index
                break

        if first_index >= 0:
            # if the first index was not set, there's nothing to move
            if last_index < first_index:
                last_index = len(self._vm_code_addresses)

            self._vm_code_list[first_index:] = (self._vm_code_list[last_index:] +
                                                self._vm_code_list[first_index:last_index])
            self.update_addresses(first_code_address)

        index = self.get_bytecode_size()
        return index

    def remove_opcodes_by_addresses(self, addresses: List[int]):
        was_changed = False
        # reversed so we only need to update addresses once after all are removed
        for code_address in sorted(addresses, reverse=True):
            try:
                index = self._vm_code_addresses.index(code_address)
                code = self._vm_code_list.pop(index)

                was_changed = True
                self._vm_code_with_target.remove(code)
            except ValueError:
                # don't stop the loop if an address is not found
                continue

        if was_changed:
            self.update_addresses(min(addresses))

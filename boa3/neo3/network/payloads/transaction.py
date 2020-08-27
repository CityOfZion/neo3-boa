import hashlib
from enum import IntEnum
from typing import List

from boa3.neo3 import settings
from boa3.neo3.core import Size as s, serialization, utils, types
from boa3.neo3.network import payloads
from boa3.neo3.vm import VMState


class TransactionAttributeUsage(IntEnum):
    URL = 0x81


class TransactionAttribute(serialization.ISerializable):
    """
    Attributes that can be attached to a Transaction.
    """

    def __init__(self, usage: TransactionAttributeUsage = None, data: bytes = None):
        self.usage = usage
        self.data = data if data else bytearray()

    def __len__(self):
        return s.uint8 + utils.get_var_size(self.data)

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_uint8(self.usage)
        writer.write_var_bytes(self.data)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.usage = TransactionAttributeUsage(reader.read_uint8())
        self.data = reader.read_var_bytes(max=252)


class Transaction(serialization.ISerializable, payloads.IInventory):
    """
    Data to be executed by the NEO virtual machine.
    """
    #: the maximum number of bytes a single transaction may consists of
    MAX_TRANSACTION_SIZE = 102400
    #: the maximum time a transaction will be valid from height of creation plus this value.
    MAX_VALID_UNTIL_BLOCK_INCREMENT = 2102400
    #: the maximum number of transaction attributes for a single transaction
    MAX_TRANSACTION_ATTRIBUTES = 16
    #: the maximum number of cosigners for a single
    MAX_COSIGNERS = 16

    def __init__(self,
                 version: int = 0,
                 nonce: int = 0,
                 sender: types.UInt160 = None,
                 system_fee: int = 0,
                 network_fee: int = 0,
                 valid_until_block: int = 0,
                 attributes: List[TransactionAttribute] = None,
                 cosigners: List[payloads.Cosigner] = None,
                 script: bytes = None,
                 witnesses: List[payloads.Witness] = None,
                 protocol_magic: int = None):
        self.version = version
        self.nonce = nonce
        #: Script hash of the first signing authority
        self.sender = sender if sender else types.UInt160.zero()
        self.system_fee = system_fee
        self.network_fee = network_fee
        self.valid_until_block = valid_until_block
        self.attributes = attributes if attributes else []
        #: A list of authorities used by the :func:`ChecKWitness` smart contract system call.
        self.cosigners = cosigners if cosigners else []
        self.script = script if script else b''
        #: A list of signing authorities used to validate the transaction.
        self.witnesses = witnesses if witnesses else []

        # unofficial attributes
        self.vm_state = VMState.NONE
        self.block_height = 0
        #: The network protocol magic number to use in the Transaction hash function. Defaults to 0x4F454E
        #: Warning: changing this will change the TX hash which can result in dangling transactions in the database as
        #: deletion and duplication checking will fail.
        if protocol_magic:
            self.protocol_magic = protocol_magic
        elif settings.network.magic is not None:
            self.protocol_magic = settings.network.magic
        else:
            self.protocol_magic = 0x4F454E

    def __len__(self):
        return (s.uint8 + s.uint32 + s.uint160 + s.uint64 + s.uint64 + s.uint32
                + utils.get_var_size(self.attributes)
                + utils.get_var_size(self.cosigners)
                + utils.get_var_size(self.script)
                + utils.get_var_size(self.witnesses))

    def __eq__(self, other):
        if other is None:
            return False
        if type(self) != type(other):
            return False
        if self.hash() != other.hash():
            return False
        return True

    def __hash__(self):
        # the TX hash() is a UInt256, we need to return an int
        # so we call hash() on the UInt256
        return hash(self.hash())

    def __deepcopy__(self, memodict={}):
        # not the best, but faster than letting deepcopy() do introspection
        with serialization.BinaryWriter() as bw:
            self.serialize_special(bw)
            with serialization.BinaryReader(bw.to_array()) as br:
                tx = Transaction()
                tx.deserialize_special(br)
                return tx

    def hash(self) -> types.UInt256:
        """
        Get a unique block identifier based on the unsigned data portion of the object.
        """
        with serialization.BinaryWriter() as bw:
            bw.write_uint32(self.protocol_magic)
            self.serialize_unsigned(bw)
            data_to_hash = bytearray(bw._stream.getvalue())
            data = hashlib.sha256(hashlib.sha256(data_to_hash).digest()).digest()
            return types.UInt256(data=data)

    @property
    def inventory_type(self) -> payloads.InventoryType:
        """
        Inventory type identifier.
        """
        return payloads.InventoryType.TX

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        self.serialize_unsigned(writer)
        writer.write_serializable_list(self.witnesses)

    def serialize_unsigned(self, writer: serialization.BinaryWriter) -> None:
        writer.write_uint8(self.version)
        writer.write_uint32(self.nonce)
        writer.write_serializable(self.sender)
        writer.write_int64(self.system_fee)
        writer.write_int64(self.network_fee)
        writer.write_uint32(self.valid_until_block)
        writer.write_serializable_list(self.attributes)
        writer.write_serializable_list(self.cosigners)
        writer.write_var_bytes(self.script)

    def serialize_special(self, writer: serialization.BinaryWriter) -> None:
        self.serialize(writer)
        writer.write_uint8(self.vm_state)
        writer.write_uint32(self.block_height)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.deserialize_unsigned(reader)
        self.witnesses = reader.read_serializable_list(payloads.Witness)

    def deserialize_unsigned(self, reader: serialization.BinaryReader) -> None:
        self.version = reader.read_uint8()
        if self.version > 0:
            raise ValueError("Deserialization error - invalid version")
        self.nonce = reader.read_uint32()
        self.sender = reader.read_serializable(types.UInt160)
        self.system_fee = reader.read_int64()
        if self.system_fee < 0:
            raise ValueError("Deserialization error - negative system fee")
        self.network_fee = reader.read_int64()
        if self.network_fee < 0:
            raise ValueError("Deserialization error - negative network fee")
        # Impossible overflow, only applicable to the C# implementation where they use longs
        # if (self.system_fee + self.network_fee < self.system_fee):
        #     raise ValueError("Deserialization error - overflow")
        self.valid_until_block = reader.read_uint32()
        self.attributes = reader.read_serializable_list(TransactionAttribute)
        self.cosigners = reader.read_serializable_list(payloads.Cosigner)
        self.script = reader.read_var_bytes(max=65535)
        if len(self.script) == 0:
            raise ValueError("Deserialization error - invalid script length 0")

    def deserialize_special(self, reader: serialization.BinaryReader) -> None:
        self.deserialize(reader)
        self.vm_state = VMState(reader.read_uint8())
        self.block_height = reader.read_uint32()

    def fee_per_byte(self) -> int:
        """
        Calculates the network fee per byte.

        Fee per byte = the TX's networkfee / TX's size

        Warning:
            Should only be called once the transaction is completely build and will no longer be modified.
        """
        return self.network_fee // len(self)

    def from_replica(self, replica):
        self.version = replica.version
        self.nonce = replica.nonce
        self.sender = replica.sender
        self.system_fee = replica.system_fee
        self.network_fee = replica.network_fee
        self.valid_until_block = replica.valid_until_block
        self.attributes = replica.attributes
        self.cosigners = replica.cosigners
        self.script = replica.script
        self.witnesses = replica.witnesses
        self.block_height = replica.block_height
        self.vm_state = replica.vm_state

    # TODO: implement Verify methods once we have Snapshot support

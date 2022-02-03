2. Tutorials
############

This section presents a few examples of Python code that can be compiled by **Neo3-Boa** into actual Smart Contracts and deployed to the Neo Blockchain. 

The main goal of these tutorials is to introduce Blockchain concepts to the Python developer. In each of them, we will try to highlight basic concepts of Smart Contract logic, pinpointing the ways in which it differs from usual programming logic, and the structural reasons behind those differences.

All of the examples presented here can be found in the `examples folder of the Neo3-Boa repository <https://github.com/CityOfZion/neo3-boa/tree/development/boa3_test/examples>`_

2.1 Hello World
===============

.. warning::
    
    **CONTENT MISSING:** Brief Tutorial Description of Hello World

::

    from boa3.builtin import NeoMetadata, metadata, public
    from boa3.builtin.interop import storage


    @public
    def Main():
        storage.put('hello', 'world')


    @metadata
    def manifest() -> NeoMetadata:
        meta = NeoMetadata()

        meta.author = "COZ in partnership with Simpli"
        meta.email = "contact@coz.io"
        meta.description = 'This is a contract example'
        return meta



2.2 Neo Token Standard (NEP-17)
===============================

.. warning::
    
    **CONTENT MISSING:** Brief Tutorial Description of NEP-17

::

    from typing import Any, Union

    from boa3.builtin import NeoMetadata, metadata, public
    from boa3.builtin.contract import Nep17TransferEvent, abort
    from boa3.builtin.interop import runtime, storage
    from boa3.builtin.interop.contract import GAS as GAS_SCRIPT, NEO as NEO_SCRIPT, call_contract
    from boa3.builtin.nativecontract.contractmanagement import ContractManagement
    from boa3.builtin.type import UInt160


    # -------------------------------------------
    # METADATA
    # -------------------------------------------

    @metadata
    def manifest_metadata() -> NeoMetadata:
        """
        Defines this smart contract's metadata information
        """
        meta = NeoMetadata()
        meta.supported_standards = ['NEP-17']
        meta.add_permission(methods=['onNEP17Payment'])

        meta.author = "Mirella Medeiros, Ricardo Prado and Lucas Uezu. COZ in partnership with Simpli"
        meta.description = "NEP-17 Example"
        meta.email = "contact@coz.io"
        return meta


    # -------------------------------------------
    # TOKEN SETTINGS
    # -------------------------------------------


    # Script hash of the contract owner
    OWNER = UInt160()
    SUPPLY_KEY = 'totalSupply'

    # Symbol of the Token
    TOKEN_SYMBOL = 'NEP17'

    # Number of decimal places
    TOKEN_DECIMALS = 8

    # Total Supply of tokens in the system
    TOKEN_TOTAL_SUPPLY = 10_000_000 * 10 ** TOKEN_DECIMALS  # 10m total supply * 10^8 (decimals)

    # Value of this NEP-17 token corresponds to NEO
    AMOUNT_PER_NEO = 10

    # Value of this NEP-17 token compared to GAS
    AMOUNT_PER_GAS = 2

    # -------------------------------------------
    # Events
    # -------------------------------------------


    on_transfer = Nep17TransferEvent


    # -------------------------------------------
    # Methods
    # -------------------------------------------


    @public(safe=True)
    def symbol() -> str:
        """
        Gets the symbols of the token.

        This string must be valid ASCII, must not contain whitespace or control characters, should be limited to uppercase
        Latin alphabet (i.e. the 26 letters used in English) and should be short (3-8 characters is recommended).
        This method must always return the same value every time it is invoked.

        :return: a short string representing symbol of the token managed in this contract.
        """
        return TOKEN_SYMBOL


    @public(safe=True)
    def decimals() -> int:
        """
        Gets the amount of decimals used by the token.

        E.g. 8, means to divide the token amount by 100,000,000 (10 ^ 8) to get its user representation.
        This method must always return the same value every time it is invoked.

        :return: the number of decimals used by the token.
        """
        return TOKEN_DECIMALS


    @public(safe=True)
    def totalSupply() -> int:
        """
        Gets the total token supply deployed in the system.

        This number must not be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
        must return 10,000,000 * 10 ^ decimals.

        :return: the total token supply deployed in the system.
        """
        return storage.get(SUPPLY_KEY).to_int()


    @public(safe=True)
    def balanceOf(account: UInt160) -> int:
        """
        Get the current balance of an address

        The parameter account must be a 20-byte address represented by a UInt160.

        :param account: the account address to retrieve the balance for
        :type account: UInt160
        """
        assert len(account) == 20
        return storage.get(account).to_int()


    @public
    def transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
        """
        Transfers an amount of NEP17 tokens from one account to another

        If the method succeeds, it must fire the `Transfer` event and must return true, even if the amount is 0,
        or from and to are the same address.

        :param from_address: the address to transfer from
        :type from_address: UInt160
        :param to_address: the address to transfer to
        :type to_address: UInt160
        :param amount: the amount of NEP17 tokens to transfer
        :type amount: int
        :param data: whatever data is pertinent to the onPayment method
        :type data: Any

        :return: whether the transfer was successful
        :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` is less than zero.
        """
        # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
        assert len(from_address) == 20 and len(to_address) == 20
        # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
        assert amount >= 0

        # The function MUST return false if the from account balance does not have enough tokens to spend.
        from_balance = storage.get(from_address).to_int()
        if from_balance < amount:
            return False

        # The function should check whether the from address equals the caller contract hash.
        # If so, the transfer should be processed;
        # If not, the function should use the check_witness to verify the transfer.
        if from_address != runtime.calling_script_hash:
            if not runtime.check_witness(from_address):
                return False

        # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
        if from_address != to_address and amount != 0:
            if from_balance == amount:
                storage.delete(from_address)
            else:
                storage.put(from_address, from_balance - amount)

            to_balance = storage.get(to_address).to_int()
            storage.put(to_address, to_balance + amount)

        # if the method succeeds, it must fire the transfer event
        on_transfer(from_address, to_address, amount)
        # if the to_address is a smart contract, it must call the contracts onPayment
        post_transfer(from_address, to_address, amount, data)
        # and then it must return true
        return True


    def post_transfer(from_address: Union[UInt160, None], to_address: Union[UInt160, None], amount: int, data: Any):
        """
        Checks if the one receiving NEP17 tokens is a smart contract and if it's one the onPayment method will be called

        :param from_address: the address of the sender
        :type from_address: UInt160
        :param to_address: the address of the receiver
        :type to_address: UInt160
        :param amount: the amount of cryptocurrency that is being sent
        :type amount: int
        :param data: any pertinent data that might validate the transaction
        :type data: Any
        """
        if not isinstance(to_address, None):  # TODO: change to 'is not None' when `is` semantic is implemented
            contract = ContractManagement.get_contract(to_address)
            if not isinstance(contract, None):  # TODO: change to 'is not None' when `is` semantic is implemented
                call_contract(to_address, 'onNEP17Payment', [from_address, amount, data])


    def mint(account: UInt160, amount: int):
        """
        Mints new tokens. This is not a NEP-17 standard method, it's only being use to complement the onPayment method

        :param account: the address of the account that is sending cryptocurrency to this contract
        :type account: UInt160
        :param amount: the amount of gas to be refunded
        :type amount: int
        :raise AssertionError: raised if amount is less than than 0
        """
        assert amount >= 0
        if amount != 0:
            current_total_supply = totalSupply()
            account_balance = balanceOf(account)

            storage.put(SUPPLY_KEY, current_total_supply + amount)
            storage.put(account, account_balance + amount)

            on_transfer(None, account, amount)
            post_transfer(None, account, amount, None)


    @public
    def verify() -> bool:
        """
        When this contract address is included in the transaction signature,
        this method will be triggered as a VerificationTrigger to verify that the signature is correct.
        For example, this method needs to be called when withdrawing token from the contract.

        :return: whether the transaction signature is correct
        """
        return runtime.check_witness(OWNER)


    @public
    def _deploy(data: Any, update: bool):
        """
        Initializes the storage when the smart contract is deployed.

        :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
        """
        if not update:
            storage.put(SUPPLY_KEY, TOKEN_TOTAL_SUPPLY)
            storage.put(OWNER, TOKEN_TOTAL_SUPPLY)

            on_transfer(None, OWNER, TOKEN_TOTAL_SUPPLY)


    @public
    def onNEP17Payment(from_address: UInt160, amount: int, data: Any):
        """
        NEP-17 affirms :"if the receiver is a deployed contract, the function MUST call onPayment method on receiver
        contract with the data parameter from transfer AFTER firing the Transfer event. If the receiver doesn't want to
        receive this transfer it MUST call ABORT." Therefore, since this is a smart contract, onPayment must exists.

        There is no guideline as to how it should verify the transaction and it's up to the user to make this verification.

        For instance, this onPayment method checks if this smart contract is receiving NEO or GAS so that it can mint a
        NEP17 token. If it's not receiving a native token, than it will abort.

        :param from_address: the address of the one who is trying to send cryptocurrency to this smart contract
        :type from_address: UInt160
        :param amount: the amount of cryptocurrency that is being sent to the this smart contract
        :type amount: int
        :param data: any pertinent data that might validate the transaction
        :type data: Any
        """
        # Use calling_script_hash to identify if the incoming token is NEO or GAS
        if runtime.calling_script_hash == NEO_SCRIPT:
            corresponding_amount = amount * AMOUNT_PER_NEO
            mint(from_address, corresponding_amount)
        elif runtime.calling_script_hash == GAS_SCRIPT:
            corresponding_amount = amount * AMOUNT_PER_GAS
            mint(from_address, corresponding_amount)
        else:
            abort()

2.3 Hashed Timelock Contract (HTLC)
===================================

.. warning::
    
    **CONTENT MISSING:** Brief Tutorial Description of HTLC

::

    from typing import Any

    from boa3.builtin import NeoMetadata, metadata, public
    from boa3.builtin.contract import abort
    from boa3.builtin.interop import runtime, storage
    from boa3.builtin.interop.contract import GAS as GAS_SCRIPT, call_contract
    from boa3.builtin.interop.crypto import hash160
    from boa3.builtin.type import UInt160


    # -------------------------------------------
    # METADATA
    # -------------------------------------------


    @metadata
    def manifest_metadata() -> NeoMetadata:
        """
        Defines this smart contract's metadata information
        """
        meta = NeoMetadata()
        return meta


    # -------------------------------------------
    # VARIABLES SETTINGS
    # -------------------------------------------


    OWNER = UInt160()
    PERSON_A: bytes = b'person a'
    PERSON_B: bytes = b'person b'
    ADDRESS_PREFIX: bytes = b'address'
    AMOUNT_PREFIX: bytes = b'amount'
    TOKEN_PREFIX: bytes = b'token'
    FUNDED_PREFIX: bytes = b'funded'

    # Number of seconds that need to pass before refunding the contract
    LOCK_TIME = 15 * 1

    NOT_INITIALIZED: bytes = b'not initialized'
    START_TIME: bytes = b'start time'
    SECRET_HASH: bytes = b'secret hash'


    # -------------------------------------------
    # Methods
    # -------------------------------------------


    @public
    def verify() -> bool:
        """
        When this contract address is included in the transaction signature,
        this method will be triggered as a VerificationTrigger to verify that the signature is correct.
        For example, this method needs to be called when withdrawing token from the contract.

        :return: whether the transaction signature is correct
        """
        return runtime.check_witness(OWNER)


    @public
    def _deploy(data: Any, update: bool):
        """
        Initializes OWNER and change values of NOT_INITIALIZED and DEPLOYED when the smart contract is deployed.

        :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
        """
        if not update:
            storage.put(OWNER, OWNER)
            storage.put(NOT_INITIALIZED, True)


    @public
    def atomic_swap(person_a_address: UInt160, person_a_token: bytes, person_a_amount: int, person_b_address: UInt160,
                    person_b_token: bytes, person_b_amount: int, secret_hash: bytes) -> bool:
        """
        Initializes the storage when the atomic swap starts.

        :param person_a_address: address of person_a
        :type person_a_address: UInt160
        :param person_a_token: person_b's desired token
        :type person_a_token: bytes
        :param person_a_amount: person_b's desired amount of tokens
        :type person_a_amount: int
        :param person_b_address: address of person_b
        :type person_b_address: bytes
        :param person_b_token: person_a's desired token
        :type person_b_token: bytes
        :param person_b_amount: person_a's desired amount of tokens
        :type person_b_amount: int
        :param secret_hash: the secret hash created by the contract deployer
        :type secret_hash: bytes

        :return: whether the deploy was successful or not
        :rtype: bool

        :raise AssertionError: raised if `person_a_address` or `person_b_address` length is not 20 or if `amount` is not
        greater than zero.
        """
        # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
        assert len(person_a_address) == 20 and len(person_b_address) == 20
        # the parameter amount must be greater than 0. If not, this method should throw an exception.
        assert person_a_amount > 0 and person_b_amount > 0

        if storage.get(NOT_INITIALIZED).to_bool() and verify():
            storage.put(ADDRESS_PREFIX + PERSON_A, person_a_address)
            storage.put(TOKEN_PREFIX + PERSON_A, person_a_token)
            storage.put(AMOUNT_PREFIX + PERSON_A, person_a_amount)
            storage.put(ADDRESS_PREFIX + PERSON_B, person_b_address)
            storage.put(TOKEN_PREFIX + PERSON_B, person_b_token)
            storage.put(AMOUNT_PREFIX + PERSON_B, person_b_amount)
            storage.put(SECRET_HASH, secret_hash)
            storage.put(NOT_INITIALIZED, False)
            storage.put(START_TIME, runtime.time)
            return True
        return False


    @public
    def onNEP17Payment(from_address: UInt160, amount: int, data: Any):
        """
        Since this is a deployed contract, transfer will be calling this onPayment method with the data parameter from
        transfer. If someone is doing a not required transfer, then ABORT will be called.

        :param from_address: the address of the one who is trying to transfer cryptocurrency to this smart contract
        :type from_address: UInt160
        :param amount: the amount of cryptocurrency that is being sent to this smart contract
        :type amount: int
        :param data: any pertinent data that may validate the transaction
        :type data: Any

        :raise AssertionError: raised if `from_address` length is not 20
        """
        # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
        if from_address is not None:
            assert len(from_address) == 20

        # this validation will verify if Neo is trying to mint GAS to this smart contract
        if from_address is None and runtime.calling_script_hash == GAS_SCRIPT:
            return

        if not storage.get(NOT_INITIALIZED).to_bool():
            # Used to check if the one who's transferring to this contract is the PERSON_A
            address = storage.get(ADDRESS_PREFIX + PERSON_A)
            # Used to check if PERSON_A already transfer to this smart contract
            funded_crypto = storage.get(FUNDED_PREFIX + PERSON_A).to_int()
            # Used to check if PERSON_A is transferring the correct amount
            amount_crypto = storage.get(AMOUNT_PREFIX + PERSON_A).to_int()
            # Used to check if PERSON_A is transferring the correct token
            token_crypto = storage.get(TOKEN_PREFIX + PERSON_A)
            if (from_address == address and
                    funded_crypto == 0 and
                    amount == amount_crypto and
                    runtime.calling_script_hash == token_crypto):
                storage.put(FUNDED_PREFIX + PERSON_A, amount)
                return
            else:
                # Used to check if the one who's transferring to this contract is the OTHER_PERSON
                address = storage.get(ADDRESS_PREFIX + PERSON_B)
                # Used to check if PERSON_B already transfer to this smart contract
                funded_crypto = storage.get(FUNDED_PREFIX + PERSON_B).to_int()
                # Used to check if PERSON_B is transferring the correct amount
                amount_crypto = storage.get(AMOUNT_PREFIX + PERSON_B).to_int()
                # Used to check if PERSON_B is transferring the correct token
                token_crypto = storage.get(TOKEN_PREFIX + PERSON_B)
                if (from_address == address and
                        funded_crypto == 0 and
                        amount == amount_crypto and
                        runtime.calling_script_hash == token_crypto):
                    storage.put(FUNDED_PREFIX + PERSON_B, amount)
                    return
        abort()


    @public
    def withdraw(secret: str) -> bool:
        """
        Deposits the contract's cryptocurrency into the person_a and person_b addresses as long as they both transferred
        to this contract and there is some time remaining

        :param secret: the private key that unlocks the transaction
        :type secret: str

        :return: whether the transfers were successful
        :rtype: bool
        """
        # Checking if PERSON_A and PERSON_B transferred to this smart contract
        funded_person_a = storage.get(FUNDED_PREFIX + PERSON_A).to_int()
        funded_person_b = storage.get(FUNDED_PREFIX + PERSON_B).to_int()
        if verify() and not refund() and hash160(secret) == storage.get(SECRET_HASH) and funded_person_a != 0 and funded_person_b != 0:
            storage.put(FUNDED_PREFIX + PERSON_A, 0)
            storage.put(FUNDED_PREFIX + PERSON_B, 0)
            storage.put(NOT_INITIALIZED, True)
            storage.put(START_TIME, 0)
            call_contract(UInt160(storage.get(TOKEN_PREFIX + PERSON_B)), 'transfer',
                          [runtime.executing_script_hash, storage.get(ADDRESS_PREFIX + PERSON_A), storage.get(AMOUNT_PREFIX + PERSON_B), None])
            call_contract(UInt160(storage.get(TOKEN_PREFIX + PERSON_A)), 'transfer',
                          [runtime.executing_script_hash, storage.get(ADDRESS_PREFIX + PERSON_B), storage.get(AMOUNT_PREFIX + PERSON_A), None])
            return True

        return False


    @public
    def refund() -> bool:
        """
        If the atomic swap didn't occur in time, refunds the cryptocurrency that was deposited in this smart contract

        :return: whether enough time has passed and the cryptocurrencies were refunded
        :rtype: bool
        """
        if runtime.time > storage.get(START_TIME).to_int() + LOCK_TIME:
            # Checking if PERSON_A transferred to this smart contract
            funded_crypto = storage.get(FUNDED_PREFIX + PERSON_A).to_int()
            if funded_crypto != 0:
                call_contract(UInt160(storage.get(TOKEN_PREFIX + PERSON_A)), 'transfer',
                              [runtime.executing_script_hash, UInt160(storage.get(ADDRESS_PREFIX + PERSON_A)), storage.get(AMOUNT_PREFIX + PERSON_A).to_int(), None])

            # Checking if PERSON_B transferred to this smart contract
            funded_crypto = storage.get(FUNDED_PREFIX + PERSON_B).to_int()
            if funded_crypto != 0:
                call_contract(UInt160(storage.get(TOKEN_PREFIX + PERSON_B)), 'transfer',
                              [runtime.executing_script_hash, storage.get(ADDRESS_PREFIX + PERSON_B), storage.get(AMOUNT_PREFIX + PERSON_B).to_int(), None])
            storage.put(FUNDED_PREFIX + PERSON_A, 0)
            storage.put(FUNDED_PREFIX + PERSON_B, 0)
            storage.put(NOT_INITIALIZED, True)
            storage.put(START_TIME, 0)
            return True
        return False


2.4 Initial Coin Offering (ICO)
===============================

.. warning::
    
    **CONTENT MISSING:** Brief Tutorial Description of ICO

::

    from typing import Any, List, Union

    from boa3.builtin import NeoMetadata, metadata, public
    from boa3.builtin.contract import Nep17TransferEvent
    from boa3.builtin.interop import runtime, storage
    from boa3.builtin.interop.contract import call_contract
    from boa3.builtin.nativecontract.contractmanagement import ContractManagement
    from boa3.builtin.nativecontract.gas import GAS as GAS_TOKEN
    from boa3.builtin.nativecontract.neo import NEO as NEO_TOKEN
    from boa3.builtin.type import UInt160


    # -------------------------------------------
    # METADATA
    # -------------------------------------------


    @metadata
    def manifest_metadata() -> NeoMetadata:
        """
        Defines this smart contract's metadata information
        """
        meta = NeoMetadata()
        meta.supported_standards = ['NEP-17']
        meta.add_permission(methods=['onNEP17Payment'])

        meta.author = "Mirella Medeiros, Ricardo Prado and Lucas Uezu. COZ in partnership with Simpli"
        meta.description = "ICO Example"
        meta.email = "contact@coz.io"
        return meta


    # -------------------------------------------
    # Storage Key Prefixes
    # -------------------------------------------


    KYC_WHITELIST_PREFIX = b'KYCWhitelistApproved'
    TOKEN_TOTAL_SUPPLY_PREFIX = b'TokenTotalSupply'
    TRANSFER_ALLOWANCE_PREFIX = b'TransferAllowancePrefix_'


    # -------------------------------------------
    # TOKEN SETTINGS
    # -------------------------------------------


    # Script hash of the contract owner
    TOKEN_OWNER = UInt160()

    # Symbol of the Token
    TOKEN_SYMBOL = 'ICO'

    # Number of decimal places
    TOKEN_DECIMALS = 8

    # Initial Supply of tokens in the system
    TOKEN_INITIAL_SUPPLY = 10_000_000 * 10 ** TOKEN_DECIMALS  # 10m total supply * 10^8 (decimals)

    # -------------------------------------------
    # Events
    # -------------------------------------------


    on_transfer = Nep17TransferEvent


    # -------------------------------------------
    # Methods
    # -------------------------------------------


    @public
    def verify() -> bool:
        """
        When this contract address is included in the transaction signature,
        this method will be triggered as a VerificationTrigger to verify that the signature is correct.
        For example, this method needs to be called when withdrawing token from the contract.

        :return: whether the transaction signature is correct
        """
        return is_administrator()


    def is_administrator() -> bool:
        """
        Validates if the invoker has administrative rights

        :return: whether the contract's invoker is an administrator
        """
        return runtime.check_witness(TOKEN_OWNER)


    def is_valid_address(address: UInt160) -> bool:
        """
        Validates if the address passed through the kyc.

        :return: whether the given address is validated by kyc
        """
        return storage.get(KYC_WHITELIST_PREFIX + address).to_int() > 0


    @public
    def _deploy(data: Any, update: bool):
        """
        Initializes the storage when the smart contract is deployed.

        :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
        """
        if not update:
            storage.put(TOKEN_TOTAL_SUPPLY_PREFIX, TOKEN_INITIAL_SUPPLY)
            storage.put(TOKEN_OWNER, TOKEN_INITIAL_SUPPLY)

            on_transfer(None, TOKEN_OWNER, TOKEN_INITIAL_SUPPLY)


    @public
    def mint(amount: int) -> bool:
        """
        Mints new tokens

        :param amount: the amount of gas to be refunded
        :type amount: int
        :return: whether the refund was successful
        """
        assert amount >= 0
        if not is_administrator():
            return False

        if amount > 0:
            current_total_supply = totalSupply()
            owner_balance = balanceOf(TOKEN_OWNER)

            storage.put(TOKEN_TOTAL_SUPPLY_PREFIX, current_total_supply + amount)
            storage.put(TOKEN_OWNER, owner_balance + amount)

        on_transfer(None, TOKEN_OWNER, amount)
        post_transfer(None, TOKEN_OWNER, amount, None)
        return True


    @public
    def refund(address: UInt160, neo_amount: int, gas_amount: int) -> bool:
        """
        Refunds an address with given Neo and Gas

        :param address: the address that have the tokens
        :type address: UInt160
        :param neo_amount: the amount of neo to be refunded
        :type neo_amount: int
        :param gas_amount: the amount of gas to be refunded
        :type gas_amount: int
        :return: whether the refund was successful
        """
        assert len(address) == 20
        assert neo_amount > 0 or gas_amount > 0

        if not is_administrator():
            return False

        if neo_amount > 0:
            result = NEO_TOKEN.transfer(runtime.calling_script_hash, address, neo_amount)
            if not result:
                # due to a current limitation in the neo3-boa, changing the condition to `not result`
                # will result in a compiler error
                return False

        if gas_amount > 0:
            result = GAS_TOKEN.transfer(runtime.calling_script_hash, address, gas_amount)
            if not result:
                # due to a current limitation in the neo3-boa, changing the condition to `not result`
                # will result in a compiler error
                return False

        return True


    # -------------------------------------------
    # Public methods from NEP-17
    # -------------------------------------------


    @public(safe=True)
    def symbol() -> str:
        """
        Gets the symbols of the token.

        This symbol should be short (3-8 characters is recommended), with no whitespace characters or new-lines and should
        be limited to the uppercase latin alphabet (i.e. the 26 letters used in English).
        This method must always return the same value every time it is invoked.

        :return: a short string symbol of the token managed in this contract.
        """
        return TOKEN_SYMBOL


    @public(safe=True)
    def decimals() -> int:
        """
        Gets the amount of decimals used by the token.

        E.g. 8, means to divide the token amount by 100,000,000 (10 ^ 8) to get its user representation.
        This method must always return the same value every time it is invoked.

        :return: the number of decimals used by the token.
        """
        return TOKEN_DECIMALS


    @public(safe=True)
    def totalSupply() -> int:
        """
        Gets the total token supply deployed in the system.

        This number mustn't be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
        must return 10,000,000 * 10 ^ decimals.

        :return: the total token supply deployed in the system.
        """
        return storage.get(TOKEN_TOTAL_SUPPLY_PREFIX).to_int()


    @public(safe=True)
    def balanceOf(account: UInt160) -> int:
        """
        Get the current balance of an address

        The parameter account should be a 20-byte address.

        :param account: the account address to retrieve the balance for
        :type account: UInt160

        :return: the token balance of the `account`
        :raise AssertionError: raised if `account` length is not 20.
        """
        assert len(account) == 20
        return storage.get(account).to_int()


    @public
    def transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
        """
        Transfers a specified amount of NEP17 tokens from one account to another

        If the method succeeds, it must fire the `transfer` event and must return true, even if the amount is 0,
        or from and to are the same address.

        :param from_address: the address to transfer from
        :type from_address: UInt160
        :param to_address: the address to transfer to
        :type to_address: UInt160
        :param amount: the amount of NEP17 tokens to transfer
        :type amount: int
        :param data: whatever data is pertinent to the onPayment method
        :type data: Any

        :return: whether the transfer was successful
        :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` if less than zero.
        """
        # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
        assert len(from_address) == 20 and len(to_address) == 20
        # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
        assert amount >= 0

        # The function MUST return false if the from account balance does not have enough tokens to spend.
        from_balance = storage.get(from_address).to_int()
        if from_balance < amount:
            return False

        # The function should check whether the from address equals the caller contract hash.
        # If so, the transfer should be processed;
        # If not, the function should use the check_witness to verify the transfer.
        if from_address != runtime.calling_script_hash:
            if not runtime.check_witness(from_address):
                return False

        # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
        if from_address != to_address and amount != 0:
            if from_balance == amount:
                storage.delete(from_address)
            else:
                storage.put(from_address, from_balance - amount)

            to_balance = storage.get(to_address).to_int()
            storage.put(to_address, to_balance + amount)

        # if the method succeeds, it must fire the transfer event
        on_transfer(from_address, to_address, amount)
        # if the to_address is a smart contract, it must call the contracts onPayment
        post_transfer(from_address, to_address, amount, data)
        # and then it must return true
        return True


    def post_transfer(from_address: Union[UInt160, None], to_address: Union[UInt160, None], amount: int, data: Any):
        """
        Checks if the one receiving NEP17 tokens is a smart contract and if it's one the onPayment method will be called

        :param from_address: the address of the sender
        :type from_address: UInt160
        :param to_address: the address of the receiver
        :type to_address: UInt160
        :param amount: the amount of cryptocurrency that is being sent
        :type amount: int
        :param data: any pertinent data that might validate the transaction
        :type data: Any
        """
        if not isinstance(to_address, None):  # TODO: change to 'is not None' when `is` semantic is implemented
            contract = ContractManagement.get_contract(to_address)
            if not isinstance(contract, None):  # TODO: change to 'is not None' when `is` semantic is implemented
                call_contract(to_address, 'onNEP17Payment', [from_address, amount, data])


    @public
    def allowance(from_address: UInt160, to_address: UInt160) -> int:
        """
        Returns the amount of tokens that the to account can transfer from the from account.

        :param from_address: the address that have the tokens
        :type from_address: UInt160
        :param to_address: the address that is authorized to use the tokens
        :type to_address: UInt160

        :return: the amount of tokens that the `to` account can transfer from the `from` account
        :raise AssertionError: raised if `from_address` or `to_address` length is not 20.
        """
        # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
        assert len(from_address) == 20 and len(to_address) == 20
        return storage.get(TRANSFER_ALLOWANCE_PREFIX + from_address + to_address).to_int()


    @public(name='transferFrom')
    def transfer_from(originator: UInt160, from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
        """
        Transfers an amount from the `from` account to the `to` account if the `originator` has been approved to transfer
        the requested amount.

        :param originator: the address where the actual token is
        :type originator: UInt160
        :param from_address: the address to transfer from with originator's approval
        :type from_address: UInt160
        :param to_address: the address to transfer to
        :type to_address: UInt160
        :param amount: the amount of NEP17 tokens to transfer
        :type amount: int
        :param data: any pertinent data that might validate the transaction
        :type data: Any

        :return: whether the transfer was successful
        :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` if less than zero.
        """
        # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
        assert len(originator) == 20 and len(from_address) == 20 and len(to_address) == 20
        # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
        assert amount >= 0

        # The function should check whether the from address equals the caller contract hash.
        # If so, the transfer should be processed;
        # If not, the function should use the check_witness to verify the transfer.
        if from_address != runtime.calling_script_hash:
            if not runtime.check_witness(from_address):
                return False

        approved_transfer_amount = allowance(originator, from_address)
        if approved_transfer_amount < amount:
            return False

        originator_balance = balanceOf(originator)
        if originator_balance < amount:
            return False

        # update allowance between originator and from
        if approved_transfer_amount == amount:
            storage.delete(TRANSFER_ALLOWANCE_PREFIX + originator + from_address)
        else:
            storage.put(TRANSFER_ALLOWANCE_PREFIX + originator + from_address, approved_transfer_amount - amount)

        # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
        if amount != 0 and from_address != to_address:
            # update originator's balance
            if originator_balance == amount:
                storage.delete(originator)
            else:
                storage.put(originator, originator_balance - amount)

            # updates to's balance
            to_balance = storage.get(to_address).to_int()
            storage.put(to_address, to_balance + amount)

        # if the method succeeds, it must fire the transfer event
        on_transfer(from_address, to_address, amount)
        # if the to_address is a smart contract, it must call the contracts onPayment
        post_transfer(from_address, to_address, amount, data)
        # and then it must return true
        return True


    @public
    def approve(originator: UInt160, to_address: UInt160, amount: int) -> bool:
        """
        Approves the to account to transfer amount tokens from the originator account.

        :param originator: the address that have the tokens
        :type originator: UInt160
        :param to_address: the address that is authorized to use the tokens
        :type to_address: UInt160
        :param amount: the amount of NEP17 tokens to transfer
        :type amount: int

        :return: whether the approval was successful
        :raise AssertionError: raised if `originator` or `to_address` length is not 20 or if `amount` if less than zero.
        """
        assert len(originator) == 20 and len(to_address) == 20
        assert amount >= 0

        if not runtime.check_witness(originator):
            return False

        if originator == to_address:
            return False

        if not is_valid_address(originator) or not is_valid_address(to_address):
            # one of the address doesn't passed the kyc yet
            return False

        if balanceOf(originator) < amount:
            return False

        storage.put(TRANSFER_ALLOWANCE_PREFIX + originator + to_address, amount)
        return True


    # -------------------------------------------
    # Public methods from KYC
    # -------------------------------------------


    @public
    def kyc_register(addresses: List[UInt160]) -> int:
        """
        Includes the given addresses to the kyc whitelist

        :param addresses: a list with the addresses to be included
        :return: the number of included addresses
        """
        included_addresses = 0
        if is_administrator():
            for address in addresses:
                if len(address) == 20:
                    kyc_key = KYC_WHITELIST_PREFIX + address
                    storage.put(kyc_key, True)
                    included_addresses += 1

        return included_addresses


    @public
    def kyc_remove(addresses: List[UInt160]) -> int:
        """
        Removes the given addresses from the kyc whitelist

        :param addresses: a list with the addresses to be removed
        :return: the number of removed addresses
        """
        removed_addresses = 0
        if is_administrator():
            for address in addresses:
                if len(address) == 20:
                    kyc_key = KYC_WHITELIST_PREFIX + address
                    storage.delete(kyc_key)
                    removed_addresses += 1

        return removed_addresses

2.5 Wrapped Token
=================

.. warning::
    
    **CONTENT MISSING:** Brief Tutorial Description of Wrapped Token

::

    from typing import Any, Union

    from boa3.builtin import CreateNewEvent, NeoMetadata, metadata, public
    from boa3.builtin.contract import Nep17TransferEvent, abort
    from boa3.builtin.interop import runtime, storage
    from boa3.builtin.interop.contract import GAS as GAS_SCRIPT, NEO as NEO_SCRIPT, call_contract
    from boa3.builtin.nativecontract.contractmanagement import ContractManagement
    from boa3.builtin.nativecontract.neo import NEO as NEO_TOKEN
    from boa3.builtin.type import UInt160


    # -------------------------------------------
    # METADATA
    # -------------------------------------------

    @metadata
    def manifest_metadata() -> NeoMetadata:
        """
        Defines this smart contract's metadata information
        """
        meta = NeoMetadata()
        meta.supported_standards = ['NEP-17']
        meta.add_permission(methods=['onNEP17Payment'])
        # this contract needs to call NEO methods
        meta.add_permission(contract='0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5')

        meta.author = "Mirella Medeiros, Ricardo Prado and Lucas Uezu. COZ in partnership with Simpli"
        meta.description = "Wrapped NEO Example"
        meta.email = "contact@coz.io"
        return meta


    # -------------------------------------------
    # TOKEN SETTINGS
    # -------------------------------------------


    # Script hash of the contract owner
    OWNER = UInt160()
    SUPPLY_KEY = 'totalSupply'

    # Symbol of the Token
    TOKEN_SYMBOL = 'zNEO'

    # Number of decimal places
    TOKEN_DECIMALS = 8

    # Total Supply of tokens in the system
    TOKEN_TOTAL_SUPPLY = 10_000_000 * 10 ** TOKEN_DECIMALS  # 10m total supply * 10^8 (decimals)

    # Allowance
    ALLOWANCE_PREFIX = b'allowance'

    # -------------------------------------------
    # Events
    # -------------------------------------------


    on_transfer = Nep17TransferEvent
    on_approval = CreateNewEvent(
        [
            ('owner', UInt160),
            ('spender', UInt160),
            ('amount', int)
        ],
        'Approval'
    )


    # -------------------------------------------
    # Methods
    # -------------------------------------------


    @public(safe=True)
    def symbol() -> str:
        """
        Gets the symbols of the token.

        This string must be valid ASCII, must not contain whitespace or control characters, should be limited to uppercase
        Latin alphabet (i.e. the 26 letters used in English) and should be short (3-8 characters is recommended).
        This method must always return the same value every time it is invoked.

        :return: a short string representing symbol of the token managed in this contract.
        """
        return TOKEN_SYMBOL


    @public(safe=True)
    def decimals() -> int:
        """
        Gets the amount of decimals used by the token.

        E.g. 8, means to divide the token amount by 100,000,000 (10 ^ 8) to get its user representation.
        This method must always return the same value every time it is invoked.

        :return: the number of decimals used by the token.
        """
        return TOKEN_DECIMALS


    @public(safe=True)
    def totalSupply() -> int:
        """
        Gets the total token supply deployed in the system.

        This number must not be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
        must return 10,000,000 * 10 ^ decimals.

        :return: the total token supply deployed in the system.
        """
        return storage.get(SUPPLY_KEY).to_int()


    @public(safe=True)
    def balanceOf(account: UInt160) -> int:
        """
        Get the current balance of an address.

        The parameter account must be a 20-byte address represented by a UInt160.

        :param account: the account address to retrieve the balance for
        :type account: bytes
        """
        assert len(account) == 20
        return storage.get(account).to_int()


    @public
    def transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
        """
        Transfers an amount of zNEO tokens from one account to another.

        If the method succeeds, it must fire the `Transfer` event and must return true, even if the amount is 0,
        or from and to are the same address.

        :param from_address: the address to transfer from
        :type from_address: UInt160
        :param to_address: the address to transfer to
        :type to_address: UInt160
        :param amount: the amount of zNEO tokens to transfer
        :type amount: int
        :param data: whatever data is pertinent to the onPayment method
        :type data: Any

        :return: whether the transfer was successful
        :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` if less than zero.
        """
        # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
        assert len(from_address) == 20 and len(to_address) == 20
        # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
        assert amount >= 0

        # The function MUST return false if the from account balance does not have enough tokens to spend.
        from_balance = storage.get(from_address).to_int()
        if from_balance < amount:
            return False

        # The function should check whether the from address equals the caller contract hash.
        # If so, the transfer should be processed;
        # If not, the function should use the check_witness to verify the transfer.
        if from_address != runtime.calling_script_hash:
            if not runtime.check_witness(from_address):
                return False

        # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
        if from_address != to_address and amount != 0:
            if from_balance == amount:
                storage.delete(from_address)
            else:
                storage.put(from_address, from_balance - amount)

            to_balance = storage.get(to_address).to_int()
            storage.put(to_address, to_balance + amount)

        # if the method succeeds, it must fire the transfer event
        on_transfer(from_address, to_address, amount)
        # if the to_address is a smart contract, it must call the contracts onPayment
        post_transfer(from_address, to_address, amount, data, True)
        # and then it must return true
        return True


    @public(name='transferFrom')
    def transfer_from(spender: UInt160, from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
        """
        A spender transfers an amount of zNEO tokens allowed from one account to another.

        If the method succeeds, it must fire the `Transfer` event and must return true, even if the amount is 0,
        or from and to are the same address.

        :param spender: the address that is trying to transfer zNEO tokens
        :type spender: UInt160
        :param from_address: the address to transfer from
        :type from_address: UInt160
        :param to_address: the address to transfer to
        :type to_address: UInt160
        :param amount: the amount of zNEO tokens to transfer
        :type amount: int
        :param data: whatever data is pertinent to the onPayment method
        :type data: Any

        :return: whether the transfer was successful
        :raise AssertionError: raised if `spender`, `from_address` or `to_address` length is not 20 or if `amount` is less
        than zero.
        """
        # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
        assert len(spender) == 20 and len(from_address) == 20 and len(to_address) == 20
        # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
        assert amount >= 0

        # The function MUST return false if the from account balance does not have enough tokens to spend.
        from_balance = storage.get(from_address).to_int()
        if from_balance < amount:
            return False

        # The function MUST return false if the from account balance does not allow enough tokens to be spent by the spender.
        allowed = allowance(from_address, spender)
        if allowed < amount:
            return False

        # The function should check whether the spender address equals the caller contract hash.
        # If so, the transfer should be processed;
        # If not, the function should use the check_witness to verify the transfer.
        if spender != runtime.calling_script_hash:
            if not runtime.check_witness(spender):
                return False

        if allowed == amount:
            storage.delete(ALLOWANCE_PREFIX + from_address + spender)
        else:
            storage.put(ALLOWANCE_PREFIX + from_address + spender, allowed - amount)

        # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
        if from_address != to_address and amount != 0:
            if from_balance == amount:
                storage.delete(from_address)
            else:
                storage.put(from_address, from_balance - amount)

            to_balance = storage.get(to_address).to_int()
            storage.put(to_address, to_balance + amount)

        # if the method succeeds, it must fire the transfer event
        on_transfer(from_address, to_address, amount)
        # if the to_address is a smart contract, it must call the contracts onPayment
        post_transfer(from_address, to_address, amount, data, True)
        # and then it must return true
        return True


    @public
    def approve(spender: UInt160, amount: int) -> bool:
        """
        Allows spender to spend from your account as many times as they want until it reaches the amount allowed.
        The allowed amount will be overwritten if this method is called once more.

        :param spender: the address that will be allowed to use your zNEO
        :type spender: UInt160
        :param amount: the total amount of zNEO that the spender can spent
        :type amount: int
        :raise AssertionError: raised if `from_address` length is not 20 or if `amount` if less than zero.
        """
        assert len(spender) == 20
        assert amount >= 0

        if balanceOf(runtime.calling_script_hash) >= amount:
            storage.put(ALLOWANCE_PREFIX + runtime.calling_script_hash + spender, amount)
            on_approval(runtime.calling_script_hash, spender, amount)
            return True
        return False


    @public
    def allowance(owner: UInt160, spender: UInt160) -> int:
        """
        Gets the amount of zNEO from the owner that can be used by the spender.

        :param owner: the address that allowed the spender to spend zNEO
        :type owner: UInt160
        :param spender: the address that can spend zNEO from the owner's account
        :type spender: UInt160
        """
        return storage.get(ALLOWANCE_PREFIX + owner + spender).to_int()


    def post_transfer(from_address: Union[UInt160, None], to_address: Union[UInt160, None], amount: int, data: Any,
                      call_onPayment: bool):
        """
        Checks if the one receiving NEP17 tokens is a smart contract and if it's one the onPayment method will be called.

        :param from_address: the address of the sender
        :type from_address: UInt160
        :param to_address: the address of the receiver
        :type to_address: UInt160
        :param amount: the amount of cryptocurrency that is being sent
        :type amount: int
        :param data: any pertinent data that might validate the transaction
        :type data: Any
        :param call_onPayment: whether onPayment should be called or not
        :type call_onPayment: bool
        """
        if call_onPayment:
            if not isinstance(to_address, None):  # TODO: change to 'is not None' when `is` semantic is implemented
                contract = ContractManagement.get_contract(to_address)
                if not isinstance(contract, None):  # TODO: change to 'is not None' when `is` semantic is implemented
                    call_contract(to_address, 'onNEP17Payment', [from_address, amount, data])


    def mint(account: UInt160, amount: int):
        """
        Mints new zNEO tokens.

        :param account: the address of the account that is sending cryptocurrency to this contract
        :type account: UInt160
        :param amount: the amount of gas to be refunded
        :type amount: int
        :raise AssertionError: raised if amount is less than than 0
        """
        assert amount >= 0
        if amount != 0:
            current_total_supply = totalSupply()
            account_balance = balanceOf(account)

            storage.put(SUPPLY_KEY, current_total_supply + amount)
            storage.put(account, account_balance + amount)

            on_transfer(None, account, amount)
            post_transfer(None, account, amount, None, True)


    @public(safe=True)
    def burn(account: UInt160, amount: int):
        """
        Burns zNEO tokens.

        :param account: the address of the account that is pulling out cryptocurrency of this contract
        :type account: UInt160
        :param amount: the amount of gas to be refunded
        :type amount: int
        :raise AssertionError: raised if `account` length is not 20, amount is less than than 0 or the account doesn't have
        enough zNEO to burn
        """
        assert len(account) == 20
        assert amount >= 0
        if runtime.check_witness(account):
            if amount != 0:
                current_total_supply = totalSupply()
                account_balance = balanceOf(account)

                assert account_balance >= amount

                storage.put(SUPPLY_KEY, current_total_supply - amount)

                if account_balance == amount:
                    storage.delete(account)
                else:
                    storage.put(account, account_balance - amount)

                on_transfer(account, None, amount)
                post_transfer(account, None, amount, None, False)

                NEO_TOKEN.transfer(runtime.executing_script_hash, account, amount)


    @public
    def verify() -> bool:
        """
        When this contract address is included in the transaction signature,
        this method will be triggered as a VerificationTrigger to verify that the signature is correct.
        For example, this method needs to be called when withdrawing token from the contract.

        :return: whether the transaction signature is correct
        """
        return runtime.check_witness(OWNER)


    @public
    def _deploy(data: Any, update: bool):
        """
        Initializes the storage when the smart contract is deployed.

        :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
        """
        if not update:
            storage.put(SUPPLY_KEY, TOKEN_TOTAL_SUPPLY)
            storage.put(OWNER, TOKEN_TOTAL_SUPPLY)

            on_transfer(None, OWNER, TOKEN_TOTAL_SUPPLY)


    @public
    def onNEP17Payment(from_address: UInt160, amount: int, data: Any):
        """
        If this smart contract receives NEO, it will mint an amount of wrapped NEO

        :param from_address: the address of the one who is trying to send cryptocurrency to this smart contract
        :type from_address: UInt160
        :param amount: the amount of cryptocurrency that is being sent to the this smart contract
        :type amount: int
        :param data: any pertinent data that might validate the transaction
        :type data: Any
        """
        # Use calling_script_hash to identify if the incoming token is NEO
        if runtime.calling_script_hash == NEO_SCRIPT:
            mint(from_address, amount)
        elif runtime.calling_script_hash == GAS_SCRIPT:
            # GAS is minted when transferring NEO
            return
        else:
            abort()

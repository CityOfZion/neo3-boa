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
    from boa3.builtin.interop.storage import put


    @public
    def Main():
        put('hello', 'world')


    @metadata
    def manifest() -> NeoMetadata:
        meta = NeoMetadata()
        meta.author = "COZ in partnership with Simpli"
        meta.email = "contact@coz.io"
        meta.description = 'This is a contract example'
        return meta



2.2 Neo Token Standard (NEP17)
==============================

.. warning::
    
    **CONTENT MISSING:** Brief Tutorial Description of NEP17

::

    from typing import Any, Union

    from boa3.builtin import NeoMetadata, metadata, public
    from boa3.builtin.contract import Nep17TransferEvent, abort
    from boa3.builtin.interop.blockchain import get_contract
    from boa3.builtin.interop.contract import GAS, NEO, call_contract
    from boa3.builtin.interop.runtime import calling_script_hash, check_witness
    from boa3.builtin.interop.storage import delete, get, put
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
    TOKEN_TOTAL_SUPPLY = 10_000_000 * 100_000_000  # 10m total supply * 10^8 (decimals)

    # Value of this NEP17 token corresponds to NEO
    AMOUNT_PER_NEO = 10

    # Value of this NEP17 token compared to GAS
    AMOUNT_PER_GAS = 2


    # -------------------------------------------
    # Events
    # -------------------------------------------


    on_transfer = Nep17TransferEvent


    # -------------------------------------------
    # Methods
    # -------------------------------------------


    @public
    def symbol() -> str:
        """
        Gets the symbols of the token.
        This string must be valid ASCII, must not contain whitespace or control characters, should be limited to uppercase
        Latin alphabet (i.e. the 26 letters used in English) and should be short (3-8 characters is recommended).
        This method must always return the same value every time it is invoked.
        :return: a short string representing symbol of the token managed in this contract.
        """
        return TOKEN_SYMBOL


    @public
    def decimals() -> int:
        """
        Gets the amount of decimals used by the token.
        E.g. 8, means to divide the token amount by 100,000,000 (10 ^ 8) to get its user representation.
        This method must always return the same value every time it is invoked.
        :return: the number of decimals used by the token.
        """
        return TOKEN_DECIMALS


    @public
    def totalSupply() -> int:
        """
        Gets the total token supply deployed in the system.
        This number must not be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
        must return 10,000,000 * 10 ^ decimals.
        :return: the total token supply deployed in the system.
        """
        return get(SUPPLY_KEY).to_int()


    @public
    def balanceOf(account: UInt160) -> int:
        """
        Get the current balance of an address
        The parameter account must be a 20-byte address represented by a UInt160.
        :param account: the account address to retrieve the balance for
        :type account: UInt160
        """
        assert len(account) == 20
        return get(account).to_int()


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
        :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` if less than zero.
        """
        # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
        assert len(from_address) == 20 and len(to_address) == 20
        # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
        assert amount >= 0

        # The function MUST return false if the from account balance does not have enough tokens to spend.
        from_balance = get(from_address).to_int()
        if from_balance < amount:
            return False

        # The function should check whether the from address equals the caller contract hash.
        # If so, the transfer should be processed;
        # If not, the function should use the check_witness to verify the transfer.
        if from_address != calling_script_hash:
            if not check_witness(from_address):
                return False

        # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
        if from_address != to_address and amount != 0:
            if from_balance == amount:
                delete(from_address)
            else:
                put(from_address, from_balance - amount)

            to_balance = get(to_address).to_int()
            put(to_address, to_balance + amount)

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
        if not isinstance(to_address, None):    # TODO: change to 'is not None' when `is` semantic is implemented
            contract = get_contract(to_address)
            if not isinstance(contract, None):      # TODO: change to 'is not None' when `is` semantic is implemented
                call_contract(to_address, 'onPayment', [from_address, amount, data])


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

            put(SUPPLY_KEY, current_total_supply + amount)
            put(account, account_balance + amount)

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
        return check_witness(OWNER)


    @public
    def deploy() -> bool:
        """
        Initializes the storage when the smart contract is deployed.
        :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
        """
        if not check_witness(OWNER):
            return False

        if get(SUPPLY_KEY).to_int() > 0:
            return False

        put(SUPPLY_KEY, TOKEN_TOTAL_SUPPLY)
        put(OWNER, TOKEN_TOTAL_SUPPLY)

        on_transfer(None, OWNER, TOKEN_TOTAL_SUPPLY)
        return True


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
        if calling_script_hash == NEO:
            corresponding_amount = amount * AMOUNT_PER_NEO
            mint(from_address, corresponding_amount)
        elif calling_script_hash == GAS:
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
    from boa3.builtin.interop.contract import call_contract
    from boa3.builtin.interop.crypto import hash160
    from boa3.builtin.interop.runtime import calling_script_hash, check_witness, executing_script_hash, get_time
    from boa3.builtin.interop.storage import get, put
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
    OTHER_PERSON: bytes = b'person b'
    ADDRESS_PREFIX: bytes = b'address'
    AMOUNT_PREFIX: bytes = b'amount'
    TOKEN_PREFIX: bytes = b'token'
    FUNDED_PREFIX: bytes = b'funded'

    # Number of seconds that need to pass before refunding the contract
    LOCK_TIME = 15 * 1

    NOT_INITIALIZED: bytes = b'not initialized'
    START_TIME: bytes = b'start time'
    SECRET_HASH: bytes = b'secret hash'
    DEPLOYED: bytes = b'deployed'


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
        return check_witness(OWNER)


    @public
    def deploy() -> bool:
        """
        Initializes OWNER and change values of NOT_INITIALIZED and DEPLOYED when the smart contract is deployed.
        :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
        """
        if not check_witness(OWNER):
            return False
        if get(DEPLOYED).to_bool():
            return False

        put(OWNER, OWNER)
        put(NOT_INITIALIZED, True)
        put(DEPLOYED, True)
        return True


    @public
    def atomic_swap(owner_address: UInt160, owner_token: bytes, owner_amount: int, other_person_address: UInt160,
                    other_person_token: bytes, other_person_amount: int, secret_hash: bytes) -> bool:
        """
        Initializes the storage when the atomic swap starts.
        :param owner_address: address of owner
        :type owner_address: UInt160
        :param owner_token: other_person's desired token
        :type owner_token: bytes
        :param owner_amount: other_person's desired amount of tokens
        :type owner_amount: int
        :param other_person_address: address of other_person
        :type other_person_address: bytes
        :param other_person_token: owner's desired token
        :type other_person_token: bytes
        :param other_person_amount: owner's desired amount of tokens
        :type other_person_amount: int
        :param secret_hash: the secret hash created by the contract deployer
        :type secret_hash: bytes
        :return: whether the deploy was successful or not
        :rtype: bool
        :raise AssertionError: raised if `owner_address` or `other_person_address` length is not 20 or if `amount` is not
        greater than zero.
        """
        # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
        assert len(owner_address) == 20 and len(other_person_address) == 20
        # the parameter amount must be greater than 0. If not, this method should throw an exception.
        assert owner_amount > 0 and other_person_amount > 0

        if get(NOT_INITIALIZED).to_bool() and verify():
            put(ADDRESS_PREFIX + OWNER, owner_address)
            put(TOKEN_PREFIX + OWNER, owner_token)
            put(AMOUNT_PREFIX + OWNER, owner_amount)
            put(ADDRESS_PREFIX + OTHER_PERSON, other_person_address)
            put(TOKEN_PREFIX + OTHER_PERSON, other_person_token)
            put(AMOUNT_PREFIX + OTHER_PERSON, other_person_amount)
            put(SECRET_HASH, secret_hash)
            put(NOT_INITIALIZED, False)
            put(START_TIME, get_time)
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
        assert len(from_address) == 20

        if not get(NOT_INITIALIZED).to_bool():
            # Used to check if the one who's transferring to this contract is the OWNER
            address = get(ADDRESS_PREFIX + OWNER)
            # Used to check if OWNER already transfer to this smart contract
            funded_crypto = get(FUNDED_PREFIX + OWNER).to_int()
            # Used to check if OWNER is transferring the correct amount
            amount_crypto = get(AMOUNT_PREFIX + OWNER).to_int()
            # Used to check if OWNER is transferring the correct token
            token_crypto = get(TOKEN_PREFIX + OWNER)
            if (from_address == address and
                    funded_crypto == 0 and
                    amount == amount_crypto and
                    calling_script_hash == token_crypto):
                put(FUNDED_PREFIX + OWNER, amount)
                return
            else:
                # Used to check if the one who's transferring to this contract is the OTHER_PERSON
                address = get(ADDRESS_PREFIX + OTHER_PERSON)
                # Used to check if OTHER_PERSON already transfer to this smart contract
                funded_crypto = get(FUNDED_PREFIX + OTHER_PERSON).to_int()
                # Used to check if OTHER_PERSON is transferring the correct amount
                amount_crypto = get(AMOUNT_PREFIX + OTHER_PERSON).to_int()
                # Used to check if OTHER_PERSON is transferring the correct token
                token_crypto = get(TOKEN_PREFIX + OTHER_PERSON)
                if (from_address == address and
                        funded_crypto == 0 and
                        amount == amount_crypto and
                        calling_script_hash == token_crypto):
                    put(FUNDED_PREFIX + OTHER_PERSON, amount)
                    return
        abort()


    @public
    def withdraw(secret: str) -> bool:
        """
        Deposits the contract's cryptocurrency into the owner and other_person addresses as long as they both transferred
        to this contract and there is some time remaining
        :param secret: the private key that unlocks the transaction
        :type secret: str
        :return: whether the transfers were successful
        :rtype: bool
        """
        # Checking if OWNER and OTHER_PERSON transferred to this smart contract
        funded_owner = get(FUNDED_PREFIX + OWNER).to_int()
        funded_other_person = get(FUNDED_PREFIX + OTHER_PERSON).to_int()
        if verify() and not refund() and hash160(secret) == get(SECRET_HASH) and funded_owner != 0 and funded_other_person != 0:
            put(FUNDED_PREFIX + OWNER, 0)
            put(FUNDED_PREFIX + OTHER_PERSON, 0)
            put(NOT_INITIALIZED, True)
            put(START_TIME, 0)
            call_contract(UInt160(get(TOKEN_PREFIX + OTHER_PERSON)), 'transfer',
                        [executing_script_hash, get(ADDRESS_PREFIX + OWNER), get(AMOUNT_PREFIX + OTHER_PERSON), ''])
            call_contract(UInt160(get(TOKEN_PREFIX + OWNER)), 'transfer',
                        [executing_script_hash, get(ADDRESS_PREFIX + OTHER_PERSON), get(AMOUNT_PREFIX + OWNER), ''])
            return True

        return False


    @public
    def refund() -> bool:
        """
        If the atomic swap didn't occur in time, refunds the cryptocurrency that was deposited in this smart contract
        :return: whether enough time has passed and the cryptocurrencies were refunded
        :rtype: bool
        """
        if get_time > get(START_TIME).to_int() + LOCK_TIME:

            # Checking if OWNER transferred to this smart contract
            funded_crypto = get(FUNDED_PREFIX + OWNER).to_int()
            if funded_crypto != 0:
                call_contract(UInt160(get(TOKEN_PREFIX + OWNER)), 'transfer',
                            [executing_script_hash, get(ADDRESS_PREFIX + OWNER), get(AMOUNT_PREFIX + OWNER)])

            # Checking if OTHER_PERSON transferred to this smart contract
            funded_crypto = get(FUNDED_PREFIX + OTHER_PERSON).to_int()
            if funded_crypto != 0:
                call_contract(UInt160(get(TOKEN_PREFIX + OTHER_PERSON)), 'transfer',
                            [executing_script_hash, get(ADDRESS_PREFIX + OTHER_PERSON), get(AMOUNT_PREFIX + OTHER_PERSON)])

            put(FUNDED_PREFIX + OWNER, 0)
            put(FUNDED_PREFIX + OTHER_PERSON, 0)
            put(NOT_INITIALIZED, True)
            put(START_TIME, 0)
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
    from boa3.builtin.interop.blockchain import get_contract
    from boa3.builtin.interop.contract import GAS, NEO, call_contract
    from boa3.builtin.interop.runtime import calling_script_hash, check_witness
    from boa3.builtin.interop.storage import delete, get, put
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
    TOKEN_INITIAL_SUPPLY = 10_000_000 * 100_000_000  # 10m total supply * 10^8 (decimals)


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
        return check_witness(TOKEN_OWNER)


    def is_valid_address(address: UInt160) -> bool:
        """
        Validates if the address passed through the kyc.
        :return: whether the given address is validated by kyc
        """
        return get(KYC_WHITELIST_PREFIX + address).to_int() > 0


    @public
    def deploy() -> bool:
        """
        Initializes the storage when the smart contract is deployed.
        :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
        """
        if not check_witness(TOKEN_OWNER):
            return False

        if get(TOKEN_TOTAL_SUPPLY_PREFIX).to_int() > 0:
            return False

        put(TOKEN_TOTAL_SUPPLY_PREFIX, TOKEN_INITIAL_SUPPLY)
        put(TOKEN_OWNER, TOKEN_INITIAL_SUPPLY)

        on_transfer(None, TOKEN_OWNER, TOKEN_INITIAL_SUPPLY)
        return True


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

            put(TOKEN_TOTAL_SUPPLY_PREFIX, current_total_supply + amount)
            put(TOKEN_OWNER, owner_balance + amount)

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
            result = call_contract(NEO, 'transfer', [calling_script_hash, address, neo_amount, None])
            if result != True:
                # due to a current limitation in the neo3-boa, changing the condition to `not result`
                # will result in a compiler error
                return False

        if gas_amount > 0:
            result = call_contract(GAS, 'transfer', [calling_script_hash, address, gas_amount, None])
            if result != True:
                # due to a current limitation in the neo3-boa, changing the condition to `not result`
                # will result in a compiler error
                return False

        return True


    # -------------------------------------------
    # Public methods from NEP5.1
    # -------------------------------------------


    @public
    def symbol() -> str:
        """
        Gets the symbols of the token.
        This symbol should be short (3-8 characters is recommended), with no whitespace characters or new-lines and should
        be limited to the uppercase latin alphabet (i.e. the 26 letters used in English).
        This method must always return the same value every time it is invoked.
        :return: a short string symbol of the token managed in this contract.
        """
        return TOKEN_SYMBOL


    @public
    def decimals() -> int:
        """
        Gets the amount of decimals used by the token.
        E.g. 8, means to divide the token amount by 100,000,000 (10 ^ 8) to get its user representation.
        This method must always return the same value every time it is invoked.
        :return: the number of decimals used by the token.
        """
        return TOKEN_DECIMALS


    @public
    def totalSupply() -> int:
        """
        Gets the total token supply deployed in the system.
        This number mustn't be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
        must return 10,000,000 * 10 ^ decimals.
        :return: the total token supply deployed in the system.
        """
        return get(TOKEN_TOTAL_SUPPLY_PREFIX).to_int()


    @public
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
        return get(account).to_int()


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
        from_balance = get(from_address).to_int()
        if from_balance < amount:
            return False

        # The function should check whether the from address equals the caller contract hash.
        # If so, the transfer should be processed;
        # If not, the function should use the check_witness to verify the transfer.
        if from_address != calling_script_hash:
            if not check_witness(from_address):
                return False

        # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
        if from_address != to_address and amount != 0:
            if from_balance == amount:
                delete(from_address)
            else:
                put(from_address, from_balance - amount)

            to_balance = get(to_address).to_int()
            put(to_address, to_balance + amount)

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
        if not isinstance(to_address, None):    # TODO: change to 'is not None' when `is` semantic is implemented
            contract = get_contract(to_address)
            if not isinstance(contract, None):      # TODO: change to 'is not None' when `is` semantic is implemented
                call_contract(to_address, 'onPayment', [from_address, amount, data])


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
        return get(TRANSFER_ALLOWANCE_PREFIX + from_address + to_address).to_int()


    @public
    def transferFrom(originator: UInt160, from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
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
        if from_address != calling_script_hash:
            if not check_witness(from_address):
                return False

        approved_transfer_amount = allowance(originator, from_address)
        if approved_transfer_amount < amount:
            return False

        originator_balance = balanceOf(originator)
        if originator_balance < amount:
            return False

        # update allowance between originator and from
        if approved_transfer_amount == amount:
            delete(TRANSFER_ALLOWANCE_PREFIX + originator + from_address)
        else:
            put(TRANSFER_ALLOWANCE_PREFIX + originator + from_address, approved_transfer_amount - amount)

        # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
        if amount != 0 and from_address != to_address:
            # update originator's balance
            if originator_balance == amount:
                delete(originator)
            else:
                put(originator, originator_balance - amount)

            # updates to's balance
            to_balance = get(to_address).to_int()
            put(to_address, to_balance + amount)

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

        if not check_witness(originator):
            return False

        if originator == to_address:
            return False

        if not is_valid_address(originator) or not is_valid_address(to_address):
            # one of the address doesn't passed the kyc yet
            return False

        if balanceOf(originator) < amount:
            return False

        put(TRANSFER_ALLOWANCE_PREFIX + originator + to_address, amount)
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
                    put(kyc_key, True)
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
                    delete(kyc_key)
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
    from boa3.builtin.interop.blockchain import get_contract
    from boa3.builtin.interop.contract import NEO, call_contract
    from boa3.builtin.interop.runtime import calling_script_hash, check_witness, executing_script_hash
    from boa3.builtin.interop.storage import delete, get, put
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
    TOKEN_TOTAL_SUPPLY = 10_000_000 * 100_000_000  # 10m total supply * 10^8 (decimals)

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


    @public
    def symbol() -> str:
        """
        Gets the symbols of the token.
        This string must be valid ASCII, must not contain whitespace or control characters, should be limited to uppercase
        Latin alphabet (i.e. the 26 letters used in English) and should be short (3-8 characters is recommended).
        This method must always return the same value every time it is invoked.
        :return: a short string representing symbol of the token managed in this contract.
        """
        return TOKEN_SYMBOL


    @public
    def decimals() -> int:
        """
        Gets the amount of decimals used by the token.
        E.g. 8, means to divide the token amount by 100,000,000 (10 ^ 8) to get its user representation.
        This method must always return the same value every time it is invoked.
        :return: the number of decimals used by the token.
        """
        return TOKEN_DECIMALS


    @public
    def totalSupply() -> int:
        """
        Gets the total token supply deployed in the system.
        This number must not be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
        must return 10,000,000 * 10 ^ decimals.
        :return: the total token supply deployed in the system.
        """
        return get(SUPPLY_KEY).to_int()


    @public
    def balanceOf(account: UInt160) -> int:
        """
        Get the current balance of an address.
        The parameter account must be a 20-byte address represented by a UInt160.
        :param account: the account address to retrieve the balance for
        :type account: bytes
        """
        assert len(account) == 20
        return get(account).to_int()


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
        from_balance = get(from_address).to_int()
        if from_balance < amount:
            return False

        # The function should check whether the from address equals the caller contract hash.
        # If so, the transfer should be processed;
        # If not, the function should use the check_witness to verify the transfer.
        if from_address != calling_script_hash:
            if not check_witness(from_address):
                return False

        # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
        if from_address != to_address and amount != 0:
            if from_balance == amount:
                delete(from_address)
            else:
                put(from_address, from_balance - amount)

            to_balance = get(to_address).to_int()
            put(to_address, to_balance + amount)

        # if the method succeeds, it must fire the transfer event
        on_transfer(from_address, to_address, amount)
        # if the to_address is a smart contract, it must call the contracts onPayment
        post_transfer(from_address, to_address, amount, data, True)
        # and then it must return true
        return True


    @public
    def transferFrom(spender: UInt160, from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
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
        :raise AssertionError: raised if `spender`, `from_address` or `to_address` length is not 20 or if `amount` if less
        than zero.
        """
        # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
        assert len(spender) == 20 and len(from_address) == 20 and len(to_address) == 20
        # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
        assert amount >= 0

        # The function MUST return false if the from account balance does not have enough tokens to spend.
        from_balance = get(from_address).to_int()
        if from_balance < amount:
            return False

        # The function MUST return false if the from account balance does not allow enough tokens to be spent by the spender.
        allowed = allowance(from_address, spender)
        if allowed < amount:
            return False

        # The function should check whether the spender address equals the caller contract hash.
        # If so, the transfer should be processed;
        # If not, the function should use the check_witness to verify the transfer.
        if spender != calling_script_hash:
            if not check_witness(spender):
                return False

        if allowed == amount:
            delete(ALLOWANCE_PREFIX + from_address + spender)
        else:
            put(ALLOWANCE_PREFIX + from_address + spender, allowed - amount)

        # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
        if from_address != to_address and amount != 0:
            if from_balance == amount:
                delete(from_address)
            else:
                put(from_address, from_balance - amount)

            to_balance = get(to_address).to_int()
            put(to_address, to_balance + amount)

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

        if balanceOf(calling_script_hash) >= amount:
            put(ALLOWANCE_PREFIX + calling_script_hash + spender, amount)
            on_approval(calling_script_hash, spender, amount)
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
        return get(ALLOWANCE_PREFIX + owner + spender).to_int()


    def post_transfer(from_address: Union[UInt160, None], to_address: Union[UInt160, None], amount: int, data: Any, call_onPayment: bool):
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
                contract = get_contract(to_address)
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

            put(SUPPLY_KEY, current_total_supply + amount)
            put(account, account_balance + amount)

            on_transfer(None, account, amount)
            post_transfer(None, account, amount, None, True)


    @public
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
        if check_witness(account):
            if amount != 0:
                current_total_supply = totalSupply()
                account_balance = balanceOf(account)

                assert account_balance >= amount

                put(SUPPLY_KEY, current_total_supply - amount)

                if account_balance == amount:
                    delete(account)
                else:
                    put(account, account_balance - amount)

                on_transfer(account, None, amount)
                post_transfer(account, None, amount, None, False)

                call_contract(NEO, 'transfer', [executing_script_hash, account, amount, None])


    @public
    def verify() -> bool:
        """
        When this contract address is included in the transaction signature,
        this method will be triggered as a VerificationTrigger to verify that the signature is correct.
        For example, this method needs to be called when withdrawing token from the contract.
        :return: whether the transaction signature is correct
        """
        return check_witness(OWNER)


    @public
    def deploy() -> bool:
        """
        Initializes the storage when the smart contract is deployed.
        :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
        """
        if not check_witness(OWNER):
            return False

        if get(SUPPLY_KEY).to_int() > 0:
            return False

        put(SUPPLY_KEY, TOKEN_TOTAL_SUPPLY)
        put(OWNER, TOKEN_TOTAL_SUPPLY)

        on_transfer(None, OWNER, TOKEN_TOTAL_SUPPLY)
        return True


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
        if calling_script_hash == NEO:
            mint(from_address, amount)
        else:
            abort()
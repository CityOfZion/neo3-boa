# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added


### Changed


### Deprecated


### Removed


### Fixed


## [1.1.1] - 2024-02-02
### Added
- Support to Python 3.12
- Included `Nep17Contract` interface
- Support to Python's builtins:
  - fstrings and match-case with primitive types (`bool`, `int` and `str`) 
  - `str.replace` and `list.sort` methods


### Deprecated
- Deprecated `@metadata` decorator to identify metadata function.


### Fixed
- Changed exit code on compilation error
- Fixed notify not being executed when calling it from the imported package
- Changed manifest abi types related to `Optional` and `Union` with `None` types


## [1.1.0] - 2023-10-16
### Added
- Support to Neo features up to Neo 3.6
  - Added zero knowledge proof methods to `CryptoLib` interface
  - Support to ASSERTMSG and ABORTMSG opcodes
- `to_hex_str` method to convert `bytes` into printable strings

### Changed
- Included `msg` optional argument to `abort`
- Validate if given `.nef` files exists before running TestRunner


### Removed
- Dropped support to Python versions prior to 3.10


### Fixed
- Removed incorrect requirement of `filelock` to use NeoTestRunner class
- Fixed imported variable value generation when it has the same identifier of a local variable
- Fixed NEP-11 validator to handle divisible NFT standard


## [1.0.0] - 2023-07-10
### Added
- Included an environment parameter to compilation that is accessible in the smart contract
- Added `hash` property to classes with `@contract` decorator
- New optional argument to stop compilation on first error found

### Changed
- Changed the cli command to compile from `neo3-boa` to `neo3-boa compile`
- Limit logs to ERROR by default
- Support to `int` constructor with `str` argument
- Change NEP-11 validator to accept both `str` and `bytes` as argument types in some methods

### Removed
- Removed [TestEngine](https://github.com/CityOfZion/neo3-boa/blob/4e3ad421ed9a85b04d70239b5d4ab3a98f2da06d/boa3_test/tests/test_classes/testengine.py) interface

### Fixed
- Fixed type warnings shown by IDEs
- Fixed Interop type check in event interfaces
- Fixed compilation to stop with keyboard interruption on cli
- Fixed compilation error with metadata and imported contract interfaces
- Fixed incorrect stack when calling `call_contract`


## [0.14.0] - 2023-06-20
> This version has breaking changes. Please refer to our [migration guide](/docs/migration-guide-v0.14.0.md) to update your smart contracts.

### Changed
- Moved `ByteString` class methods `to_int`, `to_str`, `to_bytes` and `to_bool` to the module `boa3.builtin.type.helper`

### Removed
- Removed `ByteString` type.
- Removed `to_int` implementation from `str` and `bytes` types.
- Removed `to_bytes` implementation from `int` and `bytes` types.
- Removed `to_str` implementation from `bytes` types.
- Removed `to_bool` implementation from `bytes` type.

### Fixed
- Fixed debugging information for symbols of imported modules.
- Fixed incorrect import error caused by root folder path.
- Fixed generation of static variables that were duplicated.
- Fixed code generation for method calls on `return` statements in void methods.
- Fixed compilation failure caused by imports in the file where `NeoMetadata` is defined.
- Fixed standard validations when using imported symbols.


## [0.13.1] - 2023-05-29
### Changed
- Imported contract interfaces are included on metadata permissions to ensure the expected executing behaviour 


### Fixed
- Fixed inconsistent behaviour on metadata permission


## [0.13.0] - 2023-05-08
### Added
- Included execution tests in the unit tests using the [Neo Test Runner](https://github.com/ngdenterprise/neo-test#neo-test-runner).


### Deprecated
- Deprecating [TestEngine](https://github.com/CityOfZion/neo3-boa/blob/4e3ad421ed9a85b04d70239b5d4ab3a98f2da06d/boa3_test/tests/test_classes/testengine.py) interface. 


## [0.12.3] - 2023-04-26
### Fixed
- Fixed incorrect import error raised when importing modules in the same directory of the importer file


## [0.12.2] - 2023-03-30
### Added
- Included extra data to manifest and new types to better interface with manifest
  - `Address`, `BlockHash`, `PublicKey`, `ScriptHash`, `ScriptHashLittleEndian` and `TransactionId` interfaces were included in the `boa3.builtin.type` package


### Changed
- Improving of log messages for classes, `list`s and `dict`s
- Moved compiler internal packages that are not meant to be accessed from smart contracts to `boa3.internal`


### Fixed
- Fixed incorrect behaviour when using variables with the same identifier in different scopes
- Don't generate files when internal errors are raised
- Incorrect output of `to_script_hash` when the input is a string that not represents an account address
- Type hinting didn't accept sequences with `Optional` or `Union` defining its items type
  - i.e. `List[Optional[str]]` didn't work properly


## [0.12.1] - 2023-02-15
### Added
- [CPM](https://github.com/CityOfZion/cpm) installer


## [0.12.0] - 2023-01-19
### Added
- Support to Neo features up to Neo 3.5
  - `loadScript` interop
  - Contract Management native `hasMethod` method
- Included the enum `Opcode` in the available builtin types
- Included nef `source` modifier to `NeoMetadata`
- Added `hash` property to native smart contract interfaces
- Added `hash` property to smart contract interfaces using the `@contract` decorator
- Native smart contract methods called the interfaces are now included in the manifest permissions  
- Support to `str` constructor

### Changed
- Moved the following items from `boa3.buitin`:
  - `to_script_hash` method to `boa3.builtin.contract`
  - `CreateNewEvent` method to `boa3.builtin.compile_time`
  - `NeoMetadata` class to `boa3.builtin.compile_time`
  - `public` decorator to `boa3.builtin.compile_time`
  - `metadata` decorator to `boa3.builtin.compile_time`
  - `contract` decorator to `boa3.builtin.compile_time`
  - `display_name` decorator to `boa3.builtin.compile_time`
- Native contract method calls are now called using method tokens added to the contract NEF file
- Persist the cast type of variable after the casting
- Only types or class names can be used as type annotations
  - i.e. `[int]` will fail on compilation, use `List[int]` instead


### Fixed
- Inner object variable access caused an exception to be thrown
- Invalid script was generated when compiling a smart contract with classes and `_deploy` method
- Smart contracts with methods with duplicated manifest identifiers was compiled even though the generated manifest was invalid.
- Events with the same name of some method weren't allowed by the compiler
- Internal compiler error raised when evaluating smart contract interfaces inside loops


## [0.11.4] - 2022-08-02
### Added
- Included Neo 3.2 features
  - `getAddressVersion` interop
  - CryptoLib native `murmur32` method
  - Ledger native `getTransactionVMState` and `getTransactionSigners` methods
  - Neo native `getCandidateVote`, `getAllCandidates` and `unVote` methods
- Included manifest `groups` and `trusts` modifiers to `NeoMetadata`
- Contract standards detection if not explicitly stated in the metadata
  - Supports NEO-11 and NEO-17

### Changed
- Changed `print` behavior to log readable results depending on the type of the value
- Support to `dict.pop` with the `default` argument

### Fixed
- `isinstance` and `is None` changing the type evaluated by the compiler
- Calling methods inside another method call failed in runtime


## [0.11.3] - 2022-06-13
### Added
- Support to Python 3.10
- `to_script_hash` to convert ECPoint and public keys
- `bytearray` constructor given array length


### Changed
- Updated debug file generation to map imported modules
- Included `--debug` flag information in the docs
- `x is None` and `x is not None` now have the same behaviour as `(not) isinstance(x, None)`
- Importing packages inside `boa3` in a smart contract will always raise an `UnresolvedReference` error, except for `boa3.builtin`


### Fixed
- Fixed `bytearray` set value
- Fixed bytecode generation for imported modules
- Fixed standard validators event and type checking
- Fixed global variables usage inside classes
- Fixed `int.to_bytes(0)` return to a non-empty bytes


## [0.11.2] - 2022-04-01
### Added
- New compiling option to set the project root path
- Support to `pass` keyword

### Changed
- `bool` functions that returned `Integer` values during runtime now returns actual `Boolean` values
- Logs when there are different symbols using the same identifier 


### Fixed
- Fixed Circular import detection
- Fixed an error raised when using instance methods from variables in a user-created class
- Fixed manifest generation of `ByteString` type


## [0.11.0] - 2022-02-21
### Added
- Support to contract manifest modifiers. See [NeoMetadata](https://dojo.coz.io/neo3/boa/boa3/builtin/boa3-builtins.html#boa3.builtin.NeoMetadata) 
- Initial support to inheritance on user-created classes
- Implemented Python `+` operator for lists
- Implemented implicit conversion to `bool` on if statements
- Support to Python's builtins:
  - `pow` method
  - `int` and `bool` constructors
- Implemented `builtin.math` module
  - Methods `floor` and `ceil` with decimals argument
- Implemented `ByteString` to interface when both `str` and `bytes` are supported.
  - Similar to `Union[str, bytes]`

### Changed
- Moved `boa3.builtin.sqrt` to `boa3.builtin.math.sqrt`
- `assert` message is actually logged at runtime

### Fixed
- Fixed class import with alias
- Fixed runtime errors with lists of lists
- Fixed runtime errors when using variables with the same name in classes and functions


## [0.10.1] - 2021-11-30
### Added
- Support to [Neo 3.1.0](https://github.com/neo-project/neo/tree/v3.1.0)
- Implemented class properties on user-created classes
- Support to Python 3.9
- Support to `WitnessScope`s in the TestEngine
- Implemented keyword args on function definitions
- Custom contract interfaces
- Support to Python's builtins:
  - `str` methods: `join`, `startswith`, `upper`, `lower`, `index`, `isdigit` and `strip`
  - `list` `copy` method and `dict` `pop` and `copy` methods

### Changed
- Changed operations implementation to work with custom types
- Moved `boa3.builtin.interop.blockchain.current_height` to `boa3.builtin.nativecontract.Ledger.get_current_index()` 

### Fixed
- Fixed importing from different user packages
- Fixed issue with `insert` in the first position on lists
- Fixed the runtime error raised when using instance variables
- Fixed incorrect implicit cast behavior
- Fixed incorrect code generation when calling class methods from objects


## [0.10.0] - 2021-09-13
### Added
- Support to user implemented classes
- Interfaces to N3 native contracts
- Support to wildcard imports
- Sequence slices with given strides
- Python's `max` and `min` with `str` and `bytes` arguments

### Changed
- Unified crypto methods `verify_with_ecdsa_secp256r1` and `verify_with_ecdsa_secp256k1` into `verify_with_ecdsa`
- Changed `json_serialize` return and `json_deserialize` argument types to `str`

### Fixed
- Fixed the issue with functions with the same name in different scopes
- Fixed a bug with naming variables with the same name from interop packages


## [0.9.0] - 2021-08-02
### Added
- Support to [N3-rc4](https://github.com/neo-project/neo/releases/tag/v3.0.0-rc4)
- Included new interops from Neo-rc4
  - `get_network`
  - `get_random`
- Included OracleRequestCode enum for better compatibility with Oracles
- Implemented Python's builtin `str` count
  

### Changed
- Changed manifest's `features` from an empty array to an empty object
- Included `maxsplit` optional argument on `str` split method


## [0.8.3] - 2021-07-19
### Added
- Included import of user modules
- Module variables are now linked to the contract's storage to persist their values
- Support to Python's builtins:
  - `is` keyword
  - `reversed`
  - `str.split`
  - `list.count` and `tuple.count`
- Included the remaining Neo interops in the `builtin.interop` package
- Included ECPoint type
- Included `find_options` optional argument to `Storage.Find` interop
- Included new smart contract example
  - Update Contract
- Implemented compiler validation of `try else` branch
  

### Changed
- Renamed `interop.binary` package to `interop.stdlib`
- `min` and `max` methods now accept many arguments instead of just two


### Fixed
- Fixed `isinstance` for `Contract` boa3 builtin class
- Fixed issue with not passing values to a vararg


## [0.8.2] - 2021-06-14
### Added
- Support to [N3-rc3](https://github.com/neo-project/neo/releases/tag/v3.0.0-rc3)
- Implemented varargs on function definitions
- Allow importing modules and packages
  - Only from `boa3.builtin` are accepted by the compiler
- Implemented Neo interop functions:
  - Runtime `script_container` and `burn_gas`
  - StorageContext `as_read_only`
  - Transaction interops:
    - `get_transaction`, `get_transaction_from_block` and `get_transaction_height`
- Implemented `Optional` type annotation
- Included `ON_PERSIST` and `POST_PERSIST` triggers
  

### Changed
- Updated debug info generation to [v1.2 format](https://github.com/ngdenterprise/design-notes/blob/master/NDX-DN11%20-%20NEO%20Debug%20Info%20Specification.md#v12-format-draft)
- Included `data` argument to `call_contract` and `update_contract`
- Renamed `get_time` and `get_platform` to `time` and `platform`


### Fixed
- Fixed variables access after casting types
- Fixed incorrect output when concatenation str and bytes values
- Fixed issue with control flow statements with many instructions
- Fixed issue with UInt160 and UInt256 constructors with slicing result
- Fixed unexpected result when comparing str values
- Fixed blocks and transactions hashes that TestEngine returns
- Fixed `isinstance` for boa3 builtin types
- Fixed issue with incorrect stack sizes during runtime


## [0.8.1] - 2021-05-12
### Added
- Support to [N3-rc2](https://github.com/neo-project/neo/releases/tag/v3.0.0-rc2)
- Implemented `itoa`, `atoi` and `get_block` interop methods
- Included UInt256 type
- Implemented Python built-in `sum` function
- Support to type casting


### Changed
- Included an optional `CallFlags` argument in `call_contract` method


## [0.8.0] - 2021-04-15
### Added
- Included StorageMap class
- Implemented `**` operator and `sqrt` function
- Supports `Oracle` in smart contracts
- Implemented `abs` builtin

### Fixed
- Assert statements weren't included in `.nefdbgnfo`


## [0.7.1] - 2021-03-24
### Added
- Support to [Neo 3 rc1](https://github.com/neo-project/neo/tree/v3.0.0-rc1)
- Implemented Python `in` operator for collections
- Support to reassign types to existing variables in a function's scope
- Included StorageContext to the storage interop functions
- Included new smart contract example
  - Automated Market Maker (AMM)

### Changed
- Included `eventName` argument to `notify` interop
- Renamed `trigger` method to `get_trigger`

### Fixed
- Fixed smart contract's storage access in TestEngine
- Null return in `update_contract` and `destroy_contract` interops
- `get_contract` and `create_contract` were returning contract's manifest as null
- Fixed Union type bug when used in CreateNewEvent


## [0.7.0] - 2021-02-11
### Added
- Support to [Neo 3 preview 5](https://github.com/neo-project/neo/tree/v3.0.0-preview5)
- Included `Iterator` interops
- Implemented Storage.Find interop
- Included new smart contract examples
  - Atomic Swap
  - Wrapped Token
- Included Python 3.7 unit tests in CircleCI workflow
- Implemented Python built-in functions
  - `exit`, `min` and `max`
  - `list` methods `insert` and `remove`

### Changed
- Improved compilation with `isinstance` function semantic for Python types
- Updated README file with how to use TestEngine

### Fixed
- Fixed operation validation when using non-primitive types
  - Couldn't use `UInt160` values in `bytes` operations for example
- Invalid stack size when calling void functions
- Compilation failing because of concatenation with `bytes` values
- Variable types in different scopes causing conflict during compilation
- Fixed conversion of sequence slicing with negative indexes


## [0.6.1] - 2020-12-18
### Added
- Included a NEP-17 example
- Implemented ``Union`` type annotation
- Implemented ``extend`` to bytearray values
  

### Changed
- Change Contract methods implementations to be compatible with Neo's preview4


### Fixed
- Bytes comparison was always returning False
- Get values from collection (``list``, ``dict``, ``tuple``) was returning the collection instead


## [0.6.0] - 2020-12-14
### Added
- Implemented cryptography methods
  - SHA256, RIPEMD160, HASH160 and HASH256
- Included Contract methods
  - Create, Update and Destroy contract
- Included ``base58`` and ``base64`` encoding/decoding
- New Neo Interops
  - GetExecutingScriptHash, GetEntryScriptHash and GetPlatform
- Json and Binary serialization/deserialization
- GetNotifications, for getting the list of events and values sent using ``notify()``
- Implemented a method to abort smart contract execution
- Included UInt160 type for compatibility with NEP17
- GetCurrentStorageContext, for Storage Interops
- New features in the TestEngine
  - Included call other smart contracts
  - Account witness
  - Inclusion of blocks and transactions
  

### Changed
- Improved examples' unit tests using TestEngine
- Changed ``nef`` and ``manifest`` generation to be compatible with Neo's preview4


### Fixed
- Fixed the type checking for sequence slices
- If-else branches inside each other weren't having the same execution flow as expected
- Type attribution in ``for`` variable - was getting iterable type instead of iterable's values type


### Removed
- ``is_application_trigger`` and ``is_verification_trigger`` methods


## [0.5.0] - 2020-10-27
### Added
- Converted `time`, `height`, `gasLeft` and `invocationCounter` interops
- Implemented compiler validation of `try finally` branch
- Included execution tests in the unit tests using the TestEngine from the [C# compiler](https://github.com/neo-project/neo-devpack-dotnet)

### Changed
- Replaced the markdown **Python Supported Features** table to a html table in the README


## [0.4.0] - 2020-10-01
### Added
- Included a neo3-boa's structure diagram in the README
- Added conversion of `continue` and `break` statements
- Included support to `range`
- Implemented compiler validation of `try except` statements
- Implemented `list.pop()` method
- Added `global` keyword validation
- Implemented `isinstance` method
- Support to chained assignments
- Optimization in the code generation of literal operations
- Implemented `print` method
- Converted the smart contract `call` interop
- Included an ICO example

### Changed
- Raises a compiler error if a method specifies a return type but doesn't have a return statement

### Fixed
- Compiler's exception handling when compiling a smart contract that uses unsupported or not yet implemented builtin methods
- Return value of storage's get method when the key is not found

## [0.3.0] - 2020-08-27

## [0.2.2] - 2020-08-21

## [0.2.1] - 2020-08-21

## [0.2.0] - 2020-08-21

## [0.0.3] - 2020-06-16
### Fixed
- ModuleNotFoundError that was raised when running the executable

## [0.0.2] - 2020-06-13


[Unreleased]: https://github.com/CityOfZion/neo3-boa/compare/master...staging
[1.1.1]: https://github.com/CityOfZion/neo3-boa/releases/tag/v1.1.1
[1.1.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v1.1.0
[1.0.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v1.0.0
[0.14.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.14.0
[0.13.1]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.13.1
[0.13.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.13.0
[0.12.3]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.12.3
[0.12.2]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.12.2
[0.12.1]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.12.1
[0.12.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.12.0
[0.11.4]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.11.4
[0.11.3]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.11.3
[0.11.2]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.11.2
[0.11.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.11.0
[0.10.1]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.10.1
[0.10.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.10.0
[0.9.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.9.0
[0.8.3]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.8.3
[0.8.2]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.8.2
[0.8.1]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.8.1
[0.8.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.8.0
[0.7.1]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.7.1
[0.7.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.7.0
[0.6.1]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.6.1
[0.6.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.6.0
[0.5.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.5.0
[0.4.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.4.0
[0.3.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.3.0
[0.2.2]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.2.2
[0.2.1]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.2.1
[0.2.0]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.2.0
[0.0.3]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.0.3
[0.0.2]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.0.2

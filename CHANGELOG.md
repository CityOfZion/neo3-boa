# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


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


[Unreleased]: https://github.com/CityOfZion/neo3-boa/compare/v0.8.1...HEAD
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

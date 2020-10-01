# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
- Compiler's exception handling when compiling a smart contract that uses unsupported or unimplemented builtin methods
- Return value of storage's get method when the key is not found

## [0.3.0] - 2020-08-27

## [0.2.2] - 2020-08-21

## [0.2.1] - 2020-08-21

## [0.2.0] - 2020-08-21

## [0.0.3] - 2020-06-16
### Fixed
- ModuleNotFoundError that was raised when running the executable

## [0.0.2] - 2020-06-13


[Unreleased]: https://github.com/CityOfZion/neo3-boa/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/CityOfZion/neo3-boa/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/CityOfZion/neo3-boa/compare/v0.2.2...v0.3.0
[0.2.2]: https://github.com/CityOfZion/neo3-boa/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/CityOfZion/neo3-boa/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/CityOfZion/neo3-boa/compare/v0.0.3...v0.2.0
[0.0.3]: https://github.com/CityOfZion/neo3-boa/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/CityOfZion/neo3-boa/releases/tag/v0.0.2

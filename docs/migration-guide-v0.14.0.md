# Neo3-Boa v0.14.0 Migration Guide

Welcome to the migration guide for the new version of Neo3-Boa.

This guide will assist you in migrating your code from the previous version to the latest version, which includes several improvements with debugger integration to enhance the smart contract debugging experience.

## System Requirements:

Ensure that your system meets the following requirements for the new compiler version:

Compiler Version: v0.14.0

Python 3.7 or later

## Pre-migration Preparation:

Before migrating your code, we recommend following these steps:

1. Backup your code and related files to ensure you have a copy of the previous version.

2. Familiarize yourself with the changes and improvements introduced in the new version by referring to the release notes and documentation.

## Migration Process:

* In the new version, the `ByteString` type has been removed. Update any contracts that use this type with either `bytes` or `str`, depending on the code logic and requirements.

* Most of the interop methods that previously used `ByteString` have been modified to use `bytes` instead.
    * Special attention to `storage` methods, which accepted both `bytes` and `str` as valid keys. In the new version, only `bytes` values are accepted as storage keys.

      Neo3-boa v0.14.0 has new methods to convert between types, like from `str` to `bytes`. Refer to [our docs](https://dojo.coz.io/neo3/boa/boa3/builtin/type/boa3-builtin-type.html#module-boa3.builtin.type.helper) for more details.

* Locate all instances where `ByteString` is used and replace it with the appropriate type (`bytes` or `str`).

* Review your codebase and make the necessary changes to ensure compatibility with the new version.

## Known Issues and Troubleshooting:

* ### NEP-11 Standard Validation:

    If your contracts implement the `NEP-11` standard, be aware that Neo3-Boa verifies if the methods that used to have `ByteString` type now are implemented as `Union[bytes, str]`.
    
## Testing and Feedback:

We encourage you to thoroughly test your migrated contracts in the new version and provide feedback on any issues or challenges you encounter. Your feedback will help us improve the migration process and address any inconsistent behaviors.

Remember to consult the updated documentation and resources provided by the new version to familiarize yourself with any additional changes, features, or improvements.

Thank you for choosing Neo3-Boa, and we appreciate your cooperation in migrating to the new version.

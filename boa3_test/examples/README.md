# Examples

This folder has some examples of smart contracts that are used throughout the blockchain. It's also recommended checking
the [tests](https://github.com/CityOfZion/neo3-boa/tree/development/boa3_test/tests/examples_tests), since they have 
comments describing why the methods are being called, and their expected behavior.

## AMM

The AMM (Automated Market Maker) is a smart contract that automates the process of token trading. This example was 
mainly based on [Uniswap V2](https://uniswap.org/blog/uniswap-v2/), and showcases one of the simplest implementations 
of blockchain AMMs.
It establishes a liquidity pool of two specific tokens, that are kept at a fixed ratio in the pool. Users can provide 
liquidity to the pool by sending amounts of the accepted tokens, and receiving a liquidity token that represents their 
participation in the pool. Other users can then swap the tokens directly one for the other. Liquidity providers receive 
a percentage of the fees as incentive to keep their tokens in the pool. The relative prices of the token pair varies 
according to the expected fixed ratio, and if they fluctuate away from prices on other markets, it creates an incentive 
for users to make a profit on this difference, thus returning balance to the pool.

## Hello World

It's a simple smart contract example that just puts the key-value pair `('hello': 'world')` into the storage.

## HTLC

The HTLC (Hashed TimeLock Contract) is a smart contract with the purpose of guaranteeing that two parties will uphold 
their agreements in the transaction. The transactions will be undone if one of them fails to back up on the agreement.

## ICO

The ICO (Initial Coin Offering) is kind of like a crowdfunding token. The creators offer a new token that is minted 
based on contributions received by the smart-contract. The period of time that tokens can be minted is fixed and early 
adopters usually pay less for the tokens than others.

## NEP-5

The [NEP-5](https://github.com/neo-project/proposals/blob/master/obsolete/nep-5.mediawiki) smart contract demonstrates 
the obsolete token standard for the Neo blockchain. This is deprecated, check [NEP-17](#nep-17).

## NEP-17

The [NEP-17](https://docs.neo.org/docs/en-us/develop/write/nep17.html) smart contract demonstrates the current token 
standard for the Neo blockchain.

## Update Contract

It's an example showing how to update a smart contract on the blockchain.

## Wrapped GAS/NEO

The wrapped tokens are tokens linked to the value of another token. In this case, the wrapped NEO is linked to NEO and 
wrapped GAS is linked to GAS. Both smart contracts are virtually the same, so there is only a test for the wrapped GAS.

# Building

To build one of the smart contracts above it is necessary to utilize the neo3-boa package and have the smart contract
on your device. After installing neo3-boa with pip, it's possible to compile the smart contract using the command:

```shell
> neo3-boa path/to/your/file.py
```

It's also possible to automate compilation by importing `Boa3` and using the `compile_and_save()` method on a script:

```python
from boa3.boa3 import Boa3

def main():
    Boa3.compile_and_save('path/to/smart/contract.py')

if __name__ == "main":
    main()

```

> For more detailed information on how to compile, read neo3-boas [documentation](https://dojo.coz.io/neo3/boa/getting-started.html#getting-started).

# Testing

There is more than one way to test your smart contract, e.g., deploying your contract at Neo's TestNet, but I'd argue 
that the quickest way to test would be using the NeoTestRunner. Check this [section](../../README.md#neotestrunner) on the project README.

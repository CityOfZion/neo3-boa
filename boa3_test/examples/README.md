# Examples

This folder has some examples of smart contracts that are used throughout the blockchain. It's also recommended checking
the [tests](https://github.com/CityOfZion/neo3-boa/tree/development/boa3_test/tests/examples_tests), since they have 
comments describing why the methods are being called, and their expected behaviour.

## AMM

The AMM (Automated Market Maker) is a smart contract with the goal to automatize token trading. Instead of buying from 
and selling to other users, there is a liquidity pool that stores two tokens and if the user wants to buy tokens from 
there, they can.
The example was mainly based on [Uniswap V2](https://uniswap.org/blog/uniswap-v2/)

## Hello World

It's a simple smart contract example that just puts the key-value pair `('hello': 'world')` into the storage.

## HTLC

The HTLC (Hashed TimeLock Contract) is a smart contract with the purpose of guaranteeing that two parties will uphold 
their agreements in the transaction. The transactions will be undone if one of them fails to back up on the agreement.

## ICO

The ICO (Initial Coin Offering) is kind of like a crowdfunding token. The creators make a white paper explaining why 
their token is worthwhile, and the users can help finance the token, receiving some benefits for doing so.

## NEP-5

The [NEP-5](https://github.com/neo-project/proposals/blob/master/obsolete/nep-5.mediawiki) smart contract demonstrates the obsolete token standard for the Neo blockchain. It was substituted by NEP-17.

## NEP-17

The [NEP-17](https://github.com/neo-project/proposals/pull/126/files?short_path=e39836e#diff-e39836e1dc236bd36413c0a15a41ea9f968729d1eb888b7f0d36d98bd1d2d357)
smart contract demonstrates the current token standard for the Neo blockchain.

## Update Contract

It's an example showing how to update a smart contract on the blockchain.

## Wrapped GAS/NEO

The wrapped tokens are tokens linked to the value of another token. In this case, the wrapped NEO is linked to NEO and 
wrapped GAS is linked to GAS. Both smart contracts are virtually the same, so there is only a test for the wrapped GAS.
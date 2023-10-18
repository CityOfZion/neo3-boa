<p align="center">
  <img
    src="/.github/resources/images/logo.png"
    width="200px;">
</p>

<p align="center">
  Write smart contracts for Neo3 in Python 
  <br/> Made by <b>COZ.IO</b>
</p>

<p align="center">  
  <a href="https://github.com/CityOfZion/neo3-boa"><strong>neo3-boa</strong></a> · <a href="https://github.com/CityOfZion/neo-mamba">neo-mamba</a> · <a href="https://github.com/CityOfZion/cpm">cpm</a>  </p>

<p align="center">
  <a href="https://circleci.com/gh/CityOfZion/neo3-boa/tree/master">
    <img src="https://circleci.com/gh/CityOfZion/neo3-boa.svg?style=shield" alt="CircleCI.">
  </a>
  <a href='https://coveralls.io/github/CityOfZion/neo3-boa?branch=master'>
    <img src='https://coveralls.io/repos/github/CityOfZion/neo3-boa/badge.svg?branch=master' alt='Coverage Status' />
  </a>
  <a href="https://pypi.org/project/neo3-boa/">
    <img src="https://img.shields.io/pypi/v/neo3-boa.svg" alt="PyPI.">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FCityOfZion%2Fneo3-boa%2Fmaster%2Fpyproject.toml" alt="Python Version.">
  </a>
  <a href="https://opensource.org/licenses/Apache-2.0">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="Licence.">
  </a>
</p>

<br/>

> Note: The latest release (v0.14.0) has breaking changes with contracts written using previous versions. Please refer to our [migration guide](/docs/migration-guide-v0.14.0.md) to update your smart contracts.

## Table of Contents
- [Overview](#overview)
- [Quickstart](#quickstart)
  - [Installation](#installation)
    - [Pip (Recommended)](#pip-recommended)
    - [Build from Source (Optional)](#build-from-source-optional)
- [Docs](#docs)
- [Reference Examples](#reference-examples)
- [Neo Python Suite Projects](#neo-python-suite-projects)
- [Contributing](#contributing)
- [License](#license)

## Overview

Neo3-Boa is a tool for creating Neo Smart Contracts using Python. It compiles `.py` files to `.nef` and `.manifest.json` formats for usage in the [Neo Virtual Machine](https://github.com/neo-project/neo-vm/) which is used to execute contracts on the [Neo Blockchain](https://github.com/neo-project/neo/).

Neo3-Boa is part of the Neo Python Framework, aimed to allow the full development of dApps using Python alone.

## Quickstart

Installation requires Python 3.10 or later.

### Installation

##### Make a Python 3 virtual environment and activate it:

On Linux / Mac OS:
```shell
$ python3 -m venv venv
$ source venv/bin/activate
```

On Windows:

```shell
$ python3 -m venv venv
$ venv\Scripts\activate.bat
```

##### Pip (Recommended)

###### Install Neo3-Boa using Pip:

```shell
$ pip install neo3-boa
```

##### Build from Source (Optional)
If Neo3-Boa is not available via pip, you can run it from source.

###### Clone Neo3-Boa:
```shell
$ git clone https://github.com/CityOfZion/neo3-boa.git
```
###### Install project dependencies:
```shell
$ pip install wheel
$ pip install -e .
```

## Docs
Check out our [getting started documentation](https://dojo.coz.io/neo3/boa/getting-started.html) to learn how to use the 
compiler. Also check our examples below for reference.

## Reference Examples

For an extensive collection of examples:
- [Smart contract examples](/boa3_test/examples)
- [Features tests](/boa3_test/test_sc)

## Neo Python Suite Projects

- **[Neo3-Boa](https://github.com/CityOfZion/neo3-boa)**: Python smart contracts' compiler.
- [neo3-mamba](https://github.com/CityOfZion/neo-mamba): Python SDK for interacting with Neo.

## Contributing

Checkout our [contributing file](CONTRIBUTING.md) to see how you can contribute with our project.

## License

- Open-source [Apache 2.0](https://github.com/CityOfZion/neo3-boa/blob/master/LICENSE).

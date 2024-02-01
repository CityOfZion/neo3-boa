# Contributing to Neo3-boa

Thank you for considering contributing to Neo3-boa! We're an open-source project that facilitates blockchain programming
by compiling code à la Python3 into a Neo blockchain compatible bytecode. 
Checkout the following two topics ([Product Strategy](#product-strategy) and [Project Structure](#project-structure))
to understand more about our project and how it works.

## Product Strategy

### Pure Python
We want Python developers to feel comfortable when trying Neo3-boa for the first time. It should look and behave like
regular Python. For this reason we decided to avoid adding new keywords, but use decorators and helper functions instead.

### Neo Python Framework
In the real world, simply coding a smart contract is not enough. Developers need to debug, deploy and invoke it.
Therefore, it’s important for this tool to be part of a bigger Python framework. To help the developers and avoid a bad
user experience, we need to use logs and inform errors with details.

### Testing against Neo VM
We need to ensure that the code works as expected, and the only way to do that is to run our tests against the official
Neo 3 VM. Neo organization already has a [Neo Test Runner](https://github.com/ngdenterprise/neo-test#neo-test-runner)
available to C# dApp developers. A [NeoTestRunner](boa3_test/test_drive/testrunner/neo_test_runner.py) class was
implemented in this project to facilitate testing compiled smart-contracts with Python.

### Maintenance
Create a product that is easy to maintain and upgrade. Use unit tests, typed and documented code to ensure its maintainability.

### Releases
After finishing a batch of issues, a branch will be created and those issues will be cherry-picked to be released. With
the help of [bump-my-version](https://github.com/callowayproject/bump-my-version), we update Neo3-boa's version and add a tag to indicate 
a new release, we also update the changelog detailing what has changed. The branch will be merged into the master branch 
and CircleCI will run all tests to check the integrity and will also await for approval to release this new version on 
PyPi. After approving the release, the new documentation will also be published.

## Project Structure

The diagram bellow shows the basic building blocks of the Neo3-Boa project.
<p>
  <img
    src="/.github/resources/images/diagram.png"
    width="500px;">
</p>

## New Features or Issues

If you found a problem when using Neo3-boa, or you want to suggest a feature that is missing, check the [issues page](https://github.com/CityOfZion/neo3-boa/issues)
to see if the change or bug was already reported, if not just create an [issue](https://github.com/CityOfZion/neo3-boa/issues/new/choose).

When creating a new issue, try to keep the title and description concise, and give some context of the issue, like a
snippet of the code where the problem is happening or a example of a feature, and its expected behaviour.

## Setting up your workspace

If you wish to contribute with the project by implementing a feature or fixing a bug, it's necessary to have a Python3
version equal or higher than 3.10 on your machine and install the Python packages listed inside the `requirements_dev.txt`
file, and also have the [.NET 6.0](https://dotnet.microsoft.com/en-us/download/dotnet/6.0) tools: [Neo-Express](https://github.com/neo-project/neo-express#neo-express-and-neo-trace) and [Neo Test Runner](https://github.com/ngdenterprise/neo-test#neo-test-runner)
installed.

```shell
pip install -e .[dev,test]
dotnet tool install Neo.Express --version 3.5.20 -g
dotnet tool install Neo.Test.Runner --version 3.5.17 -g
```

> Some tests will fail if you have the neo3-boa package installed. We only need the dependencies, that's why the 
> neo3-boa package is being uninstalled.


## Writing changes

Neo3-boa is divided mainly in 3 different folders:

- the `boa3/builtin` folder has the interface of the methods that can be called;
- the `boa3/internal` folder has the actual implementation of all methods, classes, and types, and the validation of script that will be compiled;
  - `boa3/internal/analyser` has the classes that will analyse and optimize the script;
  - `boa3/internal/model` has the implementations;
- the `boa3_test` folder has all the unit tests;

When implementing a new feature that will help program a smart contract, you'll probably need to add it inside
`boa3/internal` and `boa3/builtin`, but if it's a Python3 feature that Neo3-boa does not have, then you'll just have to
add it in `boa3/internal`.

> Try following PEP8 when writing your code, you can run autopep8 on your command line to format your code. 
> We recommend using it with the following flags `autopep8 -r -i -a -a .`, but beware that some imports can't be
> changed due to circular import problems.

### Tests

Always create unit tests and run them all to make sure everything is working.
This project uses CircleCI with Neo Test Runner and Neo-Express to test its features and Coveralls to track the Code 
Coverage. To run all tests run the Python script at boa3_test/tests/run_unit_tests.py.

## Submitting new features or bug fixes

After implementing a change you should create a new Pull Request, while we don't have a standard for naming branches
or commits, they should be descriptive and clear.

We have a template for Pull Requests that should automatically appear when you create a new one. It's not necessary to
fill all topics if they are not relevant to the issue you wrote.

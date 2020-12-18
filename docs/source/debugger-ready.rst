Debugger ready
==============

Neo3-boa is compatible with the `Neo Debugger`_. Debugger launch configuration example::

    {
        //Launch configuration example for Neo3-boa.
        //Make sure you compile your smart-contract before you try to debug it.
        "version": "0.2.0",
        "configurations": [
            {
                "name": "example.nef",
                "type": "neo-contract",
                "request": "launch",
                "program": "${workspaceFolder}\\example.nef",
                "operation": "main",
                "args": [],
                "storage": [],
                "runtime": {
                    "witnesses": {
                        "check-result": true
                    }
                }
            }
        ]
    }



.. _Neo Debugger: https://github.com/neo-project/neo-debugger
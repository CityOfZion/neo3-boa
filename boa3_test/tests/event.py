from dataclasses import dataclass
from typing import Self

from neo3.api import noderpc
from neo3.core import types

from boa3_test.tests import boatestcase


@dataclass
class DeployEvent(boatestcase.BoaTestEvent):
    deployed_contract: types.UInt160

    @classmethod
    def from_untyped_notification(cls, n: noderpc.Notification) -> Self:
        inner_args_types = tuple(cls.__annotations__.values())
        e = super().from_notification(n, *inner_args_types)
        return cls(e.contract, e.name, e.state, *e.state)


@dataclass
class UpdateEvent(boatestcase.BoaTestEvent):
    updated_contract: types.UInt160

    @classmethod
    def from_untyped_notification(cls, n: noderpc.Notification) -> Self:
        inner_args_types = tuple(cls.__annotations__.values())
        e = super().from_notification(n, *inner_args_types)
        return cls(e.contract, e.name, e.state, *e.state)


@dataclass
class DestroyEvent(boatestcase.BoaTestEvent):
    destroyed_contract: types.UInt160

    @classmethod
    def from_untyped_notification(cls, n: noderpc.Notification) -> Self:
        inner_args_types = tuple(cls.__annotations__.values())
        e = super().from_notification(n, *inner_args_types)
        return cls(e.contract, e.name, e.state, *e.state)

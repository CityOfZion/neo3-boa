from boa3.neo.smart_contract.notification import Notification
from boa3.neo3.core.types import UInt160


class TestRunnerNotification(Notification):
    _event_name_key = 'eventname'
    _script_hash_key = 'contract'
    _value_key = 'state'

    @classmethod
    def _get_script_from_str(cls, script: str) -> bytes:
        if isinstance(script, str):
            if script.startswith('0x'):
                str_script = script[2:]
            else:
                str_script = script
            script = UInt160.from_string(str_script).to_array()

        return script

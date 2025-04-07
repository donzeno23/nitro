from typing import Dict, Optional
from lib.nitro.strategy import ActionStrategy, HttpAction, FileReadAction, SleepAction, RecoveryAction
from lib.nitro.probes import ProbeStrategy, MetricsProbe, LoggingProbe, DebugProbe

def get_probes(probe_names: list) -> list:
    """
    Returns a list of probe objects based on the provided probe names.
    """
    probe_map = {
        'metrics': MetricsProbe(),
        'logging': LoggingProbe(),
        'debug': DebugProbe()
    }
    return [probe_map[probe_name] for probe_name in probe_names if probe_name in probe_map]


class ActionFactory:
    _strategies: Dict[str, ActionStrategy] = {
        'http': HttpAction(),
        'file_read': FileReadAction(),
        'sleep': SleepAction(),
        'recovery': RecoveryAction()
    }

    @staticmethod
    def create_action(action_type: str) -> Optional[ActionStrategy]:
        return ActionFactory._strategies.get(action_type)
        # Return None if the action type is not found

class ProbeFactory:
    """
    Factory class for creating probes to monitor or inspect test execution at certain points.
    """
    _probes: Dict[str, ProbeStrategy] = {
        'metrics': MetricsProbe(),
        'logging': LoggingProbe(),
        'debug': DebugProbe()
    }

    @staticmethod
    def create_probe(probe_type: str) -> Optional[ProbeStrategy]:
        """
        Creates and returns a probe based on the provided probe type.
        :param probe_type: The type of probe to create (e.g., 'metrics', 'logging', 'debug').
        :return: An instance of the corresponding ProbeStrategy or None if not found.
        """
        return ProbeFactory._probes.get(probe_type)
from typing import Dict, Any, List

class TestCaseBuilder:
    def __init__(self, name: str):
        self._name = name
        self._stages: List[Dict[str, Any]] = []

    def add_stage(self, stage: Dict[str, Any]) -> 'TestCaseBuilder':
        self._stages.append(stage)
        return self

    def build(self) -> Dict[str, Any]:
        return {'name': self._name, 'stages': self._stages}

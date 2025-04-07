from abc import ABC, abstractmethod
from rich import print

class ProbeStrategy(ABC):
    """
    Abstract base class for all probes.
    """
    @abstractmethod
    def execute(self):
        pass


class MetricsProbe(ProbeStrategy):
    def execute(self):
        print("[bold bright_magenta] Collecting metrics... [/bold bright_magenta]")
        # Simulate metrics collection
        print("Metrics collected successfully.")

class LoggingProbe(ProbeStrategy):
    def execute(self):
        print("Logging execution details...")


class DebugProbe(ProbeStrategy):
    def execute(self):
        print("Debugging test execution...")
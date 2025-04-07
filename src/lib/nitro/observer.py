from typing import List
from rich import print

class Observer:
    def update(self, message: str) -> None:
        pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(message)

class TestProgressObserver(Observer):
    def update(self, message: str) -> None:
        if "Skipping" in message:
            print(f"[bold blue1] Test Progress: {message} [/bold blue1]")
        elif "Executing action" in message:
            print(f"[bold dark_red] Test Progress: {message} [/bold dark_red]")
        else:
            print(f"Test Progress: {message}")

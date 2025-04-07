from abc import ABC, abstractmethod
from typing import Dict, Any
from rich import print
import time
import requests

class ActionStrategy(ABC):
    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Any:
        pass

class HttpAction(ActionStrategy):
    def execute(self, params: Dict[str, Any]) -> Any:
        url = params.get('url')
        print(f"Executing HTTP action for URL: {url}")
        # Simulate a failure for demonstration purposes
        if url == "https://simulate-failure.com":
            print("[bold red]Simulating failure for HTTP action[/bold red]")
            return False  # Simulate a failed stage
        return True  # Simulate a successful stage
        # Uncomment the following lines to make an actual HTTP request
        # try:
        #     response = requests.get(url)
        #     response.raise_for_status()
        #     return response.json()
        # except requests.exceptions.RequestException as e:
        #     return str(e)

class APIAction(ActionStrategy):
    def execute(self, params: Dict[str, Any]) -> Any:
        print(f"Executing API action with parameters: {params}")
        try:
            response = requests.get(params['url'])
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return str(e)

class FileReadAction(ActionStrategy):
    def execute(self, params: Dict[str, Any]) -> Any:
        try:
            with open(params['filepath'], 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "File not found."

class SleepAction(ActionStrategy):
    def execute(self, params: Dict[str, Any]) -> Any:
        time.sleep(params['seconds'])
        # Uncomment the following line to return a message after sleep
        # return f"Slept for {params['seconds']} seconds."
        # simulate a failure for demonstration purposes
        if params['seconds'] == 2:
            print("[bold red]Simulating failure for sleep action[/bold red]")
            return False  # Simulate a failed stage

class RecoveryAction(ActionStrategy):
    def execute(self, params: Dict[str, Any]) -> Any:
        # Simulate a recovery action. For example, restarting a service.
        print(f"Performing recovery action: {params['recovery_type']}")
        time.sleep(params.get("recovery_delay",1)) #simulate a delay
        return f"Recovery action {params['recovery_type']} completed."
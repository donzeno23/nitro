from rich import print
from typing import List, Any, Dict
from lib.nitro.factory import ActionFactory
from lib.nitro.factory import ProbeFactory
from lib.nitro.observer import Subject, TestProgressObserver
from lib.nitro.stages import get_stages, Stage

class TestOrchestrator:
    def __init__(self, stage_names: List[str], testcase_params: Dict[str, Any] = None):
        self._stage_names = stage_names
        self._subject = Subject()
        self._subject.attach(TestProgressObserver())
        self._testcase_params = testcase_params or {}
        self._stage_results: Dict[str, Any] = {}

    def execute_test(self) -> List[Any]:
        stages = get_stages(self._stage_names, self._testcase_params)
        results = []
        for stage_dict in stages:
            print("[bold yellow]*=============* Executing stage name: [/bold yellow]", stage_dict['name'])
            print("[bold yellow]*=============* Executing stage: [/bold yellow]", stage_dict)
            
            # Filter out keys not accepted by the Stage constructor
            stage_args = {key: stage_dict[key] for key in ['name', 'action', 'params', 'depends_on', 'state'] if key in stage_dict}
            stage_args['observer'] = self._subject  # Pass the observer to the Stage
            stage = Stage(**stage_args)  # Recreate the Stage object from the filtered dictionary
            # stage = Stage(**stage_dict) # Recreate the Stage object from the dictionary

            # Check if the stage has dependencies and if they are met
            # If a stage has a dependency and it is not met, skip the stage
            # and notify the observers
            # This is a simple check; in a real scenario, you might want to check the actual results of previous stages
            if stage.depends_on and stage.depends_on not in self._stage_results:
                self._subject.notify(f" **** Skipping action: {stage.name} due to unmet dependency: {stage.depends_on}")
                stage.set_state("skipped")
                results.append(f"Skipped: Dependency not met for {stage.name}")
                self._stage_results[stage.name] = f"Skipped: Dependency not met for {stage.name}"
                continue

            action_type = stage.action
            params = stage.params
            action = ActionFactory.create_action(action_type)

            metrics_probe = ProbeFactory.create_probe('metrics')
            metrics_probe.execute()

            if action:
                self._subject.notify(f"Executing action: {action_type} with params: {params}")
                try:
                    result = action.execute(params)
                    print("[bold green]Action result: [/bold green]", result)
                    if not result: # Simulate failure if the action returns False
                        # Log the result and notify observers
                        self._subject.notify(f"Action {action_type} executed successfully with result: {result}")
                        # Store the result in the stage object
                        stage.result = result
                        # Store the result in the orchestrator's results
                        self._stage_results[stage.name] = result
                        stage.set_state("failed") # Set state to "failed" if action execution fails
                        stage.error = "Action execution failed."
                        results.append("Failed: Action execution failed.")
                        raise RuntimeError("Action execution failed.")

                    results.append(result)
                    self._subject.notify(f"Action {action_type} completed.")
                    stage.set_state("completed") # Set state to "completed" after successful execution
                    stage.result = result
                    self._stage_results[stage.name] = result
                except Exception as e:
                    # Log the failure and raise an exception to fail the test case
                    self._subject.notify(f"[bold red] Action {action_type} failed with error: {str(e)} [/bold red]")
                    stage.set_state("failed") # Set state to "failed" if an exception occurs
                    stage.error = str(e)
                    self._stage_results[stage.name] = f"Failed: {str(e)}"
                    results.append(f"Failed: {str(e)}")
                    raise RuntimeError(f"Stage '{stage.name}' failed: {str(e)}")
            else:
                results.append(f"Unknown action: {action_type}")
                self._subject.notify(f"Unknown action: {action_type}")
                stage.set_state("unknown") # Set state to "unknown" if action is not found
                stage.error = f"Unknown action: {action_type}"
                self._stage_results[stage.name] = f"Unknown action: {action_type}"
        return results
        # Notify observers about the completion of all actions
        # self._subject.notify("All actions executed.")
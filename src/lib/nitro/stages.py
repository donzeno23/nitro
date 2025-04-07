from rich import print

class Stage:
    """
    Represents a single stage in the test execution pipeline.
    """
    def __init__(self, name: str, action: str, params: dict, depends_on: str = None, state: str = "not started", observer=None):
        self.name = name
        self.action = action
        self.params = params
        self.depends_on = depends_on
        self.state = state  # Initial state of the stage
        self.result = None  # Placeholder for the result of the stage execution
        self.error = None  # Placeholder for any error that occurs during execution
        self.start_time = None  # Placeholder for the start time of the stage execution
        self.end_time = None  # Placeholder for the end time of the stage execution
        self.duration = None  # Placeholder for the duration of the stage execution
        self.retry_count = 0  # Number of retries for the stage
        self.max_retries = 3  # Maximum number of retries for the stage
        self.retry_delay = 5  # Delay between retries in seconds
        self.retry_strategy = None  # Placeholder for the retry strategy
        self.retry_strategy_params = None  # Placeholder for the parameters of the retry strategy
        self.retry_strategy_result = None  # Placeholder for the result of the retry strategy
        self.retry_strategy_error = None  # Placeholder for any error that occurs during the retry strategy execution
        self.retry_strategy_start_time = None  # Placeholder for the start time of the retry strategy execution
        self.retry_strategy_end_time = None  # Placeholder for the end time of the retry strategy execution
        self.retry_strategy_duration = None  # Placeholder for the duration of the retry strategy execution
        self.retry_strategy_state = "pending"  # Initial state of the retry strategy
        self.retry_strategy_result = None  # Placeholder for the result of the retry strategy execution
        self.retry_strategy_error = None  # Placeholder for any error that occurs during the retry strategy execution
        self.observer = observer  # Reference to the observer for notifying state changes

    def set_state(self, state: str):
        """
        Sets the state of the stage (e.g., "passed", "failed").
        """
        if self.state != state:  # Only notify if the state changes
            old_state = self.state
            self.state = state
            if self.observer:
                self.observer.notify(f"Stage '{self.name}' transitioned from '{old_state}' to '{state}'")

    def to_dict(self):
        """
        Converts the Stage object to a dictionary for execution.
        """
        stage_dict = {
            'name': self.name,
            'action': self.action,
            'params': self.params,
            'state': self.state,
            'result': self.result,
            'error': self.error,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'retry_delay': self.retry_delay,
            'retry_strategy': self.retry_strategy,
            'retry_strategy_params': self.retry_strategy_params,
            'retry_strategy_result': self.retry_strategy_result,
            'retry_strategy_error': self.retry_strategy_error,
            'retry_strategy_start_time': self.retry_strategy_start_time,
            'retry_strategy_end_time': self.retry_strategy_end_time,
            'retry_strategy_duration': self.retry_strategy_duration,
            'retry_strategy_state': self.retry_strategy_state,
            'retry_strategy_result': self.retry_strategy_result,
            'retry_strategy_error': self.retry_strategy_error
        }
        if self.depends_on:
            stage_dict['depends_on'] = self.depends_on
        return stage_dict


# Pre-defined stage functions
def http_get_stage(testcase_params):
    return Stage(
        name='http_get',
        action='http',
        params={'url': testcase_params.get('http_url', 'https://httpbin.org/get')}
    )

def sleep_2s_stage(testcase_params):
    return Stage(
        name='sleep_2s',
        action='sleep',
        params={'seconds': 2}
    )

def read_file_stage(testcase_params):
    return Stage(
        name='read_file',
        action='file_read',
        params={'filepath': testcase_params.get('file_path', 'test_file.txt')}
    )

def recover_db_stage(testcase_params):
    return Stage(
        name='recover_db',
        action='recovery',
        params={'recovery_type': 'Restart Database'}
    )

def metrics_stage(testcase_params):
    return Stage(
        name='metrics_stage',
        action='sleep',
        params={'seconds': 1},
        depends_on='dependent_strategy'
    )

def graph_stage(testcase_params):
    return Stage(
        name='graphs_stage',
        action='graph',
        params={'graph_type': 'bar'},
        depends_on='metrics_stage'
    )

def report_stage(testcase_params):
    return Stage(
        name='report_stage',
        action='generate_report',
        params={'report_type': 'macro'},
        depends_on='graph_stage'
    )

# Pre-defined stage collections
# Uncomment if not using StageFactory
# PREDEFINED_STAGES = {
#     'http_get': http_get_stage,
#     'sleep_2s': sleep_2s_stage,
#     'read_file': read_file_stage,
#     'recover_db': recover_db_stage,
#     'metrics_stage': metrics_stage,
# }


# def get_stages(stage_names, testcase_params):
#     """
#     Retrieves a list of Stage objects based on the provided stage names.
#     """
#     stages = []
#     for stage_name in stage_names:
#         if stage_name in PREDEFINED_STAGES:
#             stage = PREDEFINED_STAGES[stage_name](testcase_params)
#             stages.append(stage.to_dict())  # Convert Stage object to dictionary
#         else:
#             print(f"[bold red]******* Warning: [/bold red] Stage '{stage_name}' not found. [bold red]********[/bold red]")
#     return stages

class StageFactory:
    """
    Factory class for managing the registration and retrieval of stage factories.
    """
    _factories = {}

    @classmethod
    def register_factory(cls, name: str, factory_function):
        """
        Registers a factory function for a stage.
        :param name: The name of the stage.
        :param factory_function: The factory function to create the stage.
        """
        cls._factories[name] = factory_function
        print(f"[bold green]Factory '{name}' registered successfully.[/bold green]")

    @classmethod
    def unregister_factory(cls, name: str):
        """
        Unregisters a factory function for a stage.
        :param name: The name of the stage to unregister.
        """
        if name in cls._factories:
            del cls._factories[name]
            print(f"[bold yellow]Factory '{name}' unregistered successfully.[/bold yellow]")
        else:
            print(f"[bold red]Factory '{name}' not found.[/bold red]")

    @classmethod
    def get_factory(cls, name: str):
        """
        Retrieves a factory function for a stage.
        :param name: The name of the stage.
        :return: The factory function or None if not found.
        """
        return cls._factories.get(name)

    @classmethod
    def create_stage(cls, name: str, testcase_params: dict):
        """
        Creates a stage using the registered factory function.
        :param name: The name of the stage.
        :param testcase_params: Parameters for the stage.
        :return: A Stage object or None if the factory is not registered.
        """
        factory_function = cls.get_factory(name)
        if factory_function:
            return factory_function(testcase_params)
        else:
            print(f"[bold red]Factory for stage '{name}' not found.[/bold red]")
            return None


# Register the pre-defined stage factories
StageFactory.register_factory('http_get', http_get_stage)
StageFactory.register_factory('sleep_2s', sleep_2s_stage)
StageFactory.register_factory('read_file', read_file_stage)
StageFactory.register_factory('recover_db', recover_db_stage)
StageFactory.register_factory('metrics_stage', metrics_stage)
StageFactory.register_factory('report_stage', report_stage)


def get_stages(stage_names, testcase_params):
    """
    Retrieves a list of Stage objects based on the provided stage names.
    """
    stages = []
    for stage_name in stage_names:
        stage = StageFactory.create_stage(stage_name, testcase_params)
        if stage:
            stages.append(stage.to_dict())  # Convert Stage object to dictionary
        else:
            print(f"[bold red]******* Warning: [/bold red] Stage '{stage_name}' not found. [bold red]********[/bold red]")
    return stages

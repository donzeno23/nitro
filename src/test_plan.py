import sys
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

# import testplan
from testplan.report.testing.styles import Style, StyleEnum
from testplan import test_plan
from testplan.testing.multitest import MultiTest
# from testplan.runners.pools import ThreadPool
from test_suites import PerformanceTestSuite, RecoveryTestSuite, StageExecutionSuite

from lib.nitro.orchestrator import TestOrchestrator


OUTPUT_STYLE = Style(StyleEnum.ASSERTION_DETAIL, StyleEnum.ASSERTION_DETAIL)


@test_plan(
    name='My Test Plan',
    pdf_path="report.pdf",
    stdout_style=OUTPUT_STYLE,
    pdf_style=OUTPUT_STYLE,
) # , runners=ThreadPool(workers=4))
def my_plan(plan):
    
    try:
        print("========== Creating MultiTest plan...")
        multi_test = MultiTest(
          name='Environment Setup',
          suites=[PerformanceTestSuite(), RecoveryTestSuite(), StageExecutionSuite()],
        )
        # Add the test suite to the plan
        print("========== Adding test suites...")
        plan.add(multi_test)

        # Example usage (create dummy test file)
        print("========== Creating dummy test file...")
        with open('my_file.txt', 'w') as f:
          f.write('This is a test file for the test case.')

        # NOTE: this is a dummy test case to demonstrate the orchestrator,
        # that gets executed before the Testplan testsuites
        print("========== Creating test orchestrator...")
        # Create an instance of TestOrchestrator
        test_orchestrator = TestOrchestrator(['http_get', 'sleep_2s', 'read_file', 'recover_db', 'metrics_stage'])
        print("========== Executing tests via Orchestrator...")
        results = test_orchestrator.execute_test()
        print("\n[bold orange3] Final Test Results: {results} [/bold orange3]")
        for stage_name, result in test_orchestrator._stage_results.items():
            print(f"Stage: {stage_name}, Result: {result}")

        # Return success if all stages pass
        return True

    except RuntimeError as e:
        # Log the error and return failure
        print(f"[bold red]Test failed: {e}[/bold red]")
        return False

# Example usage:
if __name__ == "__main__":

    sys.exit(not my_plan())
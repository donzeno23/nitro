import testplan
from rich import print
from testplan.runners.pools.tasks import Task
# task, runtime_values
from testplan.testing.multitest import testsuite, testcase
from lib.nitro.orchestrator import TestOrchestrator
import json
import pymongo

# @task
def run_test(testcase_name: str, stage_names: list, testcase_params: dict):
    """
    Executes the test stages using the TestOrchestrator.
    """
    orchestrator = TestOrchestrator(stage_names, testcase_params)
    results = orchestrator.execute_test()
    # runtime_values(results=results)
    return results # Return results for further processing

def performance_test(env, result, testcase, stage_names: list, http_url:str = "https://httpbin.org/ip", file_path:str = "my_file.txt"):
    """
    Executes a performance test by running the specified stages.
    """
    print("\n *********** Running performance test...")

    testcase_params = {"http_url": http_url, "file_path": file_path}
    results = run_test(testcase.__name__, stage_names, testcase_params)
    for res in results:
        result.log(str(res))

    # Save results to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["test_results"]
    col = db["results"]
    col.insert_one({"testcase_name": testcase.__name__, "results": [str(r) for r in results]})


def recovery_test(env, result, testcase, stage_names: list, http_url: str = "https://httpbin.org/ip", file_path: str = "my_file.txt"):
    print("\n *********** Running recovery test...")
    orchestrator = TestOrchestrator(stage_names, {"http_url": http_url, "file_path": file_path})
    results = orchestrator.execute_test()
    for res in results:
        result.log(str(res))
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["test_results"]
    col = db["results"]
    col.insert_one({"testcase_name": testcase.__name__, "results": [str(r) for r in results]})

@testsuite
class PerformanceTestSuite:
    @testcase(name="performance_test_case_1")
    def test_case_1(self, env, result):
        print("*********** Running performance test case 1...")
        performance_test(env, result, testcase, ['http_get', 'sleep_2s', 'dependent_stage'])

    @testcase(name="throughput_test_case_2")
    def test_case_2_with_throughput(self, env, result):
        print("*********** Running performance test case 2...")
        performance_test(env, result, testcase, ['read_file', 'recover_db'])


@testsuite
class RecoveryTestSuite:
    @testcase(name="recovery_test_case_1")
    def test_case_1(self, env, result):
        print("*********** Running recovery test case 1...")
        recovery_test(env, result, testcase, ['http_get', 'sleep_2s', 'dependent_stage'])

    @testcase(name="recovery_test_case_2")
    def test_case_2_with_recovery(self, env, result):
        print("*********** Running recovery test case 2...")
        recovery_test(env, result, testcase, ['read_file', 'recover_db'])


@testsuite
class StageExecutionSuite:
    # def __init__(self, stage_names: list, testcase_params: dict):
    def __init__(self):
        # self.test_orchestrator = TestOrchestrator()
        # self.testcase_params = testcase_params
        # self.testcase_params = {}
        self.testcase_params = {"http_url": "XXXXXXXXXXXXXXXXXXXXXX", "file_path": "my_file.txt"}
        self.results = []
        # self.stage_names = stage_names
        # self.stage_names = []
        self.stage_names = ['http_get', 'sleep_2s', 'dependent_stage']
        self.stage_results = {}
        self.stage_errors = {}
        self.stage_retries = {}
        self.stage_retry_strategy = {}
        self.stage_retry_strategy_result = {}
        self.stage_retry_strategy_error = {}
        self.stage_recovery_strategy = {}
        self.stage_recovery_strategy_result = {}
        self.stage_recovery_strategy_error = {}

    @testcase(name="stage_execution_test_case")
    def execute_stages(self, env, result):
        """
        Executes the stages using the TestOrchestrator.
        """
        print("*********** Running stage execution test case...")
        self.results = self.test_orchestrator.execute_test()
        for res in self.results:
            result.log(str(res))
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["test_results"]
        col = db["results"]
        col.insert_one({"testcase_name": "stage_execution_test_case", "results": [str(r) for r in self.results]})

    @testcase(name="stage_execution_test_case_2")
    def execute_stages_2(self, env, result):
        """
        Executes the stages using the TestOrchestrator.
        """
        test_orchestrator = TestOrchestrator(self.stage_names, self.testcase_params)
        try:
            results = test_orchestrator.execute_test()
            result.true(all(r != "Failed: Action execution failed." for r in results), "All stages passed")
        except RuntimeError as e:
            result.fail(f"Test failed: {e}")
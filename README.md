# nitro
Test toolkit

# Example Output

**On Success:**

```text
Running Testplan [My Test Plan]
Stage Execution Test
  StageExecutionSuite
    execute_stages ... Passed

Testplan finished execution
```

**On Failure:**

```text
Running Testplan [My Test Plan]
Stage Execution Test
  StageExecutionSuite
    execute_stages ... Failed
      Test failed: Stage 'sleep_2s' failed: Action execution failed.

Testplan finished execution
```
# Test a prediction that spends long time, so add this command argument to enable
# test tasks. If not provided, these tests are skipped.
def pytest_addoption(parser):
    parser.addoption("--test-hg-tasks", action="store_true", default=False)

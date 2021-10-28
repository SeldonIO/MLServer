from click.testing import CliRunner

from mlserver.cli.main import root


def test_version_does_not_error():
    runner = CliRunner()

    result = runner.invoke(root, ["--version"])

    assert result.exit_code == 0
    assert result.exception is None

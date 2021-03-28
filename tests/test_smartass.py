
from click.testing import CliRunner

from smartass import cli


def test_import():
    __import__('smartass')


def test_cli_smartass():
    runner = CliRunner()
    result = runner.invoke(cli.smartass, [])

    assert result.exit_code == 0


def test_cli_dumbass():
    runner = CliRunner()
    result = runner.invoke(cli.dumbass, [])

    assert result.exit_code == 0


def test_dummy():
    assert True is not False
    assert True

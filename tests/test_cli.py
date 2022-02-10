from click.testing import CliRunner
from plagiarism.cli import main


class TestClass:
    def test_compate(self):
        runner = CliRunner()
        result = runner.invoke(main, ['compare', '-t', 'the Big Bang singularity'])
        assert result.exit_code == 0

    def test_file(self):
        runner = CliRunner()
        result = runner.invoke(main, ['compare', '-f', 'test_input.txt'])
        assert result.exit_code == 0

    def test_compare_url(self):
        runner = CliRunner()
        result = runner.invoke(main, ['compare', '-w', 'https://en.wikipedia.org/wiki/Big_Bang', '-d', 'big bang'])
        assert result.exit_code == 0

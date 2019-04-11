import os
from pathlib import Path
import subprocess
from typing import Union
import unittest
import time


PROJECT_NAME = 'PintaFormas'

SKIP_MYPY_TEST = os.environ.get('TEST_SKIPS_MYPY') == '1'

def execute(commands: Union[list[str], str]) -> str:
    process = subprocess.run(commands, encoding="utf-8", stdout=subprocess.PIPE)
    return process.stdout


class TestCallMypy(unittest.TestCase):
    @unittest.skipIf(SKIP_MYPY_TEST, "Skipping test_call_mypy() because of TEST_SKIPS_MYPY=1")
    def test_call_mypy(self) -> None:
        t = time.time()
        project_path = Path(__file__).parents[2]
        assert Path(project_path).name == PROJECT_NAME
        result = execute(['mypy', str(project_path)])
        assert result.startswith('Success'), "\n" + result
        print("\nTiempo transcurrido ejecutando mypy:", time.time() - t, "segundos")


if __name__ == '__main__':
    unittest.main()

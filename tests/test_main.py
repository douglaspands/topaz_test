import os
from unittest.mock import patch

import config

config.FILE_INPUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "files", "input.txt")
)
config.FILE_OUTPUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "files", "output.txt")
)

from topaz_test import __main__


def test_main_1_success():

    expect_rc = 0
    rc = __main__.main()
    assert rc == expect_rc


def test_main_2_fail():

    expect_rc = 1
    with patch(
        "topaz_test.__main__.ServerManager.new_task_for_each_user",
        side_effect=Exception("mocked error"),
    ) as mock:
        rc = __main__.main()
    assert rc == expect_rc
import os
from unittest.mock import patch

import config

config.FILE_INPUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "files", "input.txt")
)
config.FILE_OUTPUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "files", "output.txt")
)


def test_main_1_success():

    from topaz_test import __main__

    expect_rc = 0
    rc = __main__.main()
    assert rc == expect_rc


def test_main_2_fail():

    from topaz_test import __main__

    expect_rc = 1
    with patch(
        "topaz_test.__main__.ServerManager.new_task_for_each_user",
        side_effect=Exception("mocked error"),
    ):
        rc = __main__.main()
    assert rc == expect_rc


def test_main_init_success():

    from topaz_test import __main__

    expect_return_code = 0

    with patch.object(__main__, "main", return_value=0):
        with patch.object(__main__, "__name__", "__main__"):
            with patch.object(__main__.sys, "exit") as mock_exit:
                __main__.init()
                assert mock_exit.call_args[0][0] == expect_return_code


def test_main_init_error():

    from topaz_test import __main__

    expect_return_code = 1

    with patch.object(__main__, "main", return_value=1):
        with patch.object(__main__, "__name__", "__main__"):
            with patch.object(__main__.sys, "exit") as mock_exit:
                __main__.init()
                assert mock_exit.call_args[0][0] == expect_return_code

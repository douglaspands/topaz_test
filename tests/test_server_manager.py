from decimal import Decimal

import pytest
from server_manager import User, Server, ServerManager


def test_user_check_instance():
    ttask = 4
    user = User(ttask=ttask)
    assert user.left_ticks == ttask


def test_user_check_negative_left_ticks():
    ttask = 4
    user = User(ttask=ttask)
    for i in range(ttask + ttask):
        assert user.remove_tick() >= 0


def test_user_check_ttask():
    ttask = 4
    user = User(ttask=ttask)
    assert user.left_ticks == ttask


def test_server_check_instance():
    umax = 2
    expect_left_ticks = 0
    expect_users = 0
    server = Server(umax=umax)
    assert server.left_ticks == expect_left_ticks
    assert server.limit_users == umax
    assert isinstance(server.users, list)
    assert len(server.users) == expect_users


def test_server_check_space_true():
    umax = 2
    ttask = 4
    expect_left_ticks = 4
    expect_users = 1
    expect_has_space = True
    server = Server(umax=umax)
    server.add_user(ttask=ttask)
    assert server.left_ticks == expect_left_ticks
    assert server.has_space == expect_users
    assert len(server.users) == expect_has_space


def test_server_check_space_false():
    umax = 2
    ttask = 4
    expect_left_ticks = 8
    expect_users = 2
    expect_has_space = False
    server = Server(umax=umax)
    for i in range(umax):
        server.add_user(ttask=ttask)
    assert server.left_ticks == expect_left_ticks
    assert server.has_space == expect_has_space
    assert len(server.users) == expect_users


def test_server_remove_tick():
    umax = 2
    ttask = 4
    expect_left_ticks = 6
    expect_users = 2
    server = Server(umax=umax)
    for i in range(umax):
        server.add_user(ttask=ttask)
    left_ticks = server.remove_tick()
    assert server.left_ticks == left_ticks
    assert server.left_ticks == expect_left_ticks
    assert len(server.users) == expect_users


def test_server_check_negative_left_ticks():
    umax = 2
    expect_left_ticks = 0
    server = Server(umax=umax)
    left_ticks = server.remove_tick()
    assert server.left_ticks == left_ticks
    assert server.left_ticks == expect_left_ticks


def test_server_remove_tick_clean():
    umax = 2
    ttask = 4
    expect_left_ticks = 0
    expect_users = 0
    server = Server(umax=umax)
    for i in range(umax):
        server.add_user(ttask=ttask)
    left_ticks = server.remove_tick()
    for i in range(server.left_ticks + 5):
        left_ticks = server.remove_tick()
    assert server.left_ticks == left_ticks
    assert server.left_ticks == expect_left_ticks
    assert len(server.users) == expect_users


def test_servermanager_instance():
    umax = 2
    ttask = 4
    expect_servers = 0
    expect_amount = 0
    server_manager = ServerManager(umax=umax, ttask=ttask)
    assert server_manager.ttask == ttask
    assert server_manager.umax == umax
    assert len(server_manager.servers) == expect_servers
    assert server_manager.amount == expect_amount


def test_servermanager_instance_ttask_error_1():
    umax = 2
    ttask = "4"
    with pytest.raises(Exception):
        ServerManager(umax=umax, ttask=ttask)


def test_servermanager_instance_umax_error_1():
    umax = "2"
    ttask = 4
    with pytest.raises(Exception):
        ServerManager(umax=umax, ttask=ttask)


def test_servermanager_has_busy_server_false():
    umax = 2
    ttask = 4
    expect_busy_server = False
    server_manager = ServerManager(umax=umax, ttask=ttask)
    assert server_manager.has_busy_server == expect_busy_server


def test_servermanager_has_busy_server_true():
    umax = 2
    ttask = 4
    expect_busy_server = True
    server_manager = ServerManager(umax=umax, ttask=ttask)
    server_manager._add_task()
    assert server_manager.has_busy_server == expect_busy_server


def test_servermanager_add_task_1_server():
    umax = 2
    ttask = 4
    amount_users = 2
    expect_report = "2"
    server_manager = ServerManager(umax=umax, ttask=ttask)
    report = server_manager.new_task_for_each_user(amount_users=amount_users)
    assert report == expect_report


def test_servermanager_add_task_2_servers():
    umax = 2
    ttask = 4
    amount_users = 3
    expect_report = "2,1"
    server_manager = ServerManager(umax=umax, ttask=ttask)
    report = server_manager.new_task_for_each_user(amount_users=amount_users)
    assert report == expect_report


def test_servermanager_add_task_1_server_error():
    umax = 2
    ttask = 4
    amount_users = "2"
    server_manager = ServerManager(umax=umax, ttask=ttask)
    with pytest.raises(Exception):
        server_manager.new_task_for_each_user(amount_users=amount_users)


def test_servermanager_free_1_server():
    umax = 2
    ttask = 2
    amount_users = [1, 2, 0, 1]
    expect_reports = ["1", "2,1", "1,1", "1"]
    server_manager = ServerManager(umax=umax, ttask=ttask)
    for i in range(len(amount_users)):
        report = server_manager.new_task_for_each_user(amount_users=amount_users[i])
        assert report == expect_reports[i]


def test_servermanager_free_all_server():
    umax = 2
    ttask = 2
    amount_users = [1, 2, 0, 1]
    expect_reports = ["1", "2,1", "1,1", "1", "1", "0"]
    expect_report_zero = "0"
    expect_amount = Decimal("7")
    server_manager = ServerManager(umax=umax, ttask=ttask)
    for i in range(len(amount_users)):
        report = server_manager.new_task_for_each_user(amount_users=amount_users[i])
        assert report == expect_reports[i]
    for i in range(len(amount_users), len(expect_reports)):
        report = server_manager.use_report
        assert report == expect_reports[i]
    assert server_manager.amount == expect_amount
    report = server_manager.use_report
    assert report == expect_report_zero
    assert server_manager.amount == expect_amount
    report = server_manager.use_report
    assert report == expect_report_zero
    assert server_manager.amount == expect_amount

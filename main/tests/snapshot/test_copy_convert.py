import pytest
import mock
from pexpect import pxssh

from main.main_lib.snapshot.copy_convert import Connection


@mock.patch('pexpect.pxssh.pxssh.login')
def test_backup_partition(mock_login):
    mock_login.return_value = True
    conn = Connection(hostname='10.1.2.217', password='@four123')
    assert conn.status is True


@mock.patch('pexpect.pxssh.pxssh.login')
def test_backup_partition_when_login_is_false_should_return_exception(mock_login):
    mock_login.side_effect = pxssh.ExceptionPxssh

    conn = Connection(hostname='10.1.2.217', password='nopasswd')
    assert conn.status

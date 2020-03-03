import os, sys, pytest, mock
from mock import mock_open, MagicMock
from main.main_lib.snapshot.smart_backup import md5, chunks_md5, size_of_file, num_process_creation


@pytest.fixture(scope='module')
def ret_file_path():
    file = os.path.abspath('dummy_test_file')
    return file


@mock.patch('builtins.open', new_callable=mock_open, read_data=b'This\nis\nmocked\nfile\n')
def test_md5_when_fname_is_provided_should_return_hexdigit(m, ret_file_path):
    assert md5(ret_file_path) == '4d16ffe4859ea62d591cb936e448e47d'
    assert m.assert_called_with(ret_file_path, 'rb') is None


def test_chunks_md5_when_str_is_provided_shoud_return_hexdigit(ret_file_path):
    assert chunks_md5(b'This string need to be tested.') == '1dc81443e1b15f9afeea97b54d698e85'


def test_size_of_file_when_provided_should_return_file_size(ret_file_path):
    m = MagicMock()
    m.seek.return_value = 20
    assert size_of_file(m) == 20


def test_num_process_creation_when_size_is_kb_returns_one():
    assert num_process_creation(2 ** 10) == pow(2, 0)


def test_num_process_creation_when_size_is_mb_returns_two():
    assert num_process_creation(2 ** 20) == pow(2, 1)


def test_num_process_creation_when_size_is_gb_returns_three():
    assert num_process_creation(2 ** 30) == pow(2, 2)

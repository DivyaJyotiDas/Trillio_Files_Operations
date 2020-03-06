from django.urls import reverse, resolve
import pytest


@pytest.mark.parametrize('inputs, expected', [
                            ('partition_list', '/api/partitions/list'),
                            ('backup_list', '/api/backup/list'),
                            ('backup_create', '/api/backup/create')
                            ])
def test_urlpatterns_when_viewname_is_provided_should_return_url(inputs, expected):
    url = reverse(viewname=inputs)
    assert url == expected


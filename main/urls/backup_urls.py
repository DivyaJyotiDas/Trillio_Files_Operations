
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from Trillio_Files_Operations.settings import base
from main.views.views import MyView, home, BackupView

urlpatterns = [
    path(r'', home, name='home'),
    path(r'partitions/list', MyView.as_view(), name='partition_list'),
    path(r'backup/list', BackupView.as_view(), name='backup_list'),
    path(r'backup/create', BackupView.as_view(), name='backup_create'),
] + static(base.STATIC_URL, document_root=base.STATIC_ROOT)

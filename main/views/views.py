import datetime
import logging
import time
from multiprocessing import Process

from django.shortcuts import render
from django.utils import timezone
from filelock import FileLock
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
# Create your views here.
from rest_framework.views import APIView

from main.main_lib.snapshot.copy_convert import Connection
from main.main_lib.snapshot.smart_backup import size_of_file, read_file
from main.models import JobExecution

Log = logging.getLogger(__name__)


class MyView(APIView):
    """
        * This View is responsible for returning partitions.
        * It Connects to the host using the creds with [Root user]
        * It triggers the library in snapshot packages.
        * Creates a context and send the Response.

        200:- Successful Operations.
        400:- Unsuccessful Operations.
    """

    def get(self, request):
        """

        :param request: Request Object.
        :return: list of Dict.
        """
        Log.info(request.data)
        req = request.GET
        hostname = req.get('hostname')
        password = req.get('password')
        with Connection(hostname=hostname, username='root', password=password) as conn:
            if not conn():
                return Response({'status': 'Hostname doesnt exists/down'}, status=HTTP_400_BAD_REQUEST)
            context = conn.get_partition()
            return Response(context, status=HTTP_200_OK)


class BackupView(APIView):
    """
        * Back up the partitions based on the key
        * smart = True
                - Invokes crude logic of multi-processing of file contents.
                - Read Operations.
                - Write Operations.
        * smart = False
                - It Invokes dd operations.
                - Single Thread invocations.
    """

    def get(self, request):
        """

        :param request: (HttpRequest)Request Object
        :return: List of Dict.
        """
        res = []
        job_all_obj = JobExecution.objects.all()
        for i in job_all_obj:
            res.append({
                'job_id': i.job_id,
                'job_name': i.job_name,
                'author': i.author,
                'start_time': i.start_time,
                'end_time': i.end_time,
                'status': i.status,
                'progress': i.progress
            })
        return Response(res, status=HTTP_200_OK)

    def post(self, request):
        """

        :param request: HttpRequest
        :return:
        """
        req = request.data
        print(req)
        T1_DEST_FILE = '/home/afour/PycharmProjects/Trillio_Files_Operations/logs/vda_one.img'
        hostname = req.get('hostname')
        passwd = req.get('password')
        author = req.get('author')
        smart_backup = req.get('smartBackup')
        source_partition = req.get('sourcePartition')

        import os
        newpid = os.fork()

        if newpid == 0:
            Log.info('Child Process Starts...')

            if not smart_backup:
                with Connection(hostname=hostname, username='root', password=passwd) as conn:
                    pid = conn.backup_partition(source_partition)
                    print('pid', pid)
                    job = JobExecution(
                        job_id=pid,
                        job_name=datetime.datetime.now(),
                        author=author,
                        end_time=None,
                        status='IN-PROGRESS',
                        progress='0'
                    )
                job.save()

                pid_job = JobExecution.objects.get(job_id=pid)

                while conn.check_if_pid_exists(pid):
                    print("TRue...")
                    backup_progress = conn.return_backup_progress(pid)
                    print(backup_progress)

                    pid_job.progress = backup_progress[0] + '#' + backup_progress[1]
                    pid_job.save(update_fields=['progress'])
                    time.sleep(5)

                if not conn.check_if_pid_exists(pid):
                    print("False...")
                    pid_job.status = 'COMPLETED'
                    pid_job.save(update_fields=['status'])

                pid_job.end_time = timezone.now()
                pid_job.save(update_fields=['end_time'])
            else:
                try:
                    job = JobExecution(
                        job_id=None,
                        job_name=datetime.datetime.now(),
                        author=author,
                        end_time=None,
                        status='IN-PROGRESS',
                        progress='0'
                    )
                    job.save()
                except Exception as e:
                    print(e)
                pid = JobExecution.objects.latest('id')._get_pk_val()
                print(pid)
                pid_job = JobExecution.objects.get(id=pid)
                print(pid_job)
                with FileLock(source_partition):
                    fp1 = open(source_partition, 'rb')
                    fp2 = open(source_partition, 'rb')
                with FileLock(T1_DEST_FILE):
                    dest_fp_1 = open(T1_DEST_FILE, 'wb+')
                    dest_fp_2 = open(T1_DEST_FILE, 'wb+')

                p1 = Process(target=read_file, args=(fp1, 0, size_of_file(fp1) // 2, dest_fp_1, pid_job))
                p2 = Process(target=read_file, args=(fp2, size_of_file(fp1) // 2, size_of_file(fp1), dest_fp_2, pid_job))

                p1.start()
                p2.start()

                p1.join()
                p2.join()

            os._exit(0)  # Exiting Child Process.

        else:
            try:
                return Response({'status': 'success'},
                                status=HTTP_200_OK)
            except Exception as e:
                return Response({'status': 'Fail'},
                                status=HTTP_400_BAD_REQUEST)


def home(request):
    return render(request, template_name='core/login.html', context={'username': 'Divya Das'})

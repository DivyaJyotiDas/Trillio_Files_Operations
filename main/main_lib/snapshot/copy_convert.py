########################
# Date- 22 Feb, 2020   #
#######################


from pexpect import pxssh

__author__ = 'Divya Das'


class Connection:
    """
        This Connection Class is responsible for cteating connection object for given hostname.
    """
    def __init__(self, hostname, password, username='root'):
        try:
            self._ssh = pxssh.pxssh()
            self.hostname = hostname
            self.username = username
            self.password = password
            self.status = True
            self._ssh.login(hostname, username, password, quiet=True)
        except pxssh.ExceptionPxssh as e:
            self.status = False

    def __call__(self, *args, **kwargs):
        return False if not self.status else True

    def __enter__(self):
        return self

    def get_partition(self):
        """
        This will fetch all the partitions return by blkid command.
        :return: list of partition available.
        """
        try:
            command = 'blkid | cut -d ":" -f1'  # 'pvs | sed "1d" | cut -d " " -f3'
            self._ssh.sendline(command)  # run a command
            self._ssh.prompt()  # match the prompt
            return [part for part in
                    self._ssh.before.decode('utf-8').splitlines()[1:]]  # print everything before the prompt.
        except OSError as oe:
            return False

    def backup_partition(self, part_name, backup_location='backup.img'):
        """
        This will backup source partition on destination partition.
        :param part_name: source partion name
        :param backup_location:  backup.img
        :return: process id.
        """
        command = 'dd if=' + part_name + ' of=' + backup_location + ' &'
        self._ssh.sendline(command)  # run a command
        self._ssh.prompt()
        pid = self._ssh.before.decode('utf-8').split('\n')[1].split(' ')[1].split('\r')[0]
        self._ssh.prompt()
        return pid

    def return_backup_progress(self, pid):
        """
        This method is responsible for checking progress of process.
        :param pid: int
        :return: tuple
        """
        percent, space = None, None
        command2 = 'progress -p ' + pid
        self._ssh.sendline(command2)  # run a command
        self._ssh.prompt()
        try:
            res = self._ssh.before.decode('utf-8').split('\t')[1].split('\r')[0].split(sep=' ', maxsplit=1)
            percent, space = res[0], res[1]
            return percent, space
        except IndexError as ie:
            percent, space = '100%', 'completed'
            return percent, space

    def check_if_pid_exists(self, pid):
        """
        Thi method checks regularly if process exists or not.
        If thr pid exists, It meand it still in progress.
        If the pid doesnt exists, It means it has finished backup of partitons.
        :param pid: int
        :return: bool
        """
        command = 'progress -p ' + pid
        self._ssh.sendline(command)  # run a command
        self._ssh.prompt()
        print(self._ssh.before)
        if 'No such pid'.lower() in self._ssh.before.decode('utf-8').split(':', maxsplit=1)[0].lower():
            return False
        return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        After completing/exceptions, It should properly close the connection.
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self._ssh.logout()



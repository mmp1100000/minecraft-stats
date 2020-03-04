import ftplib
import gzip
import uuid

default_connection_settings = {
    'server_name': 'fr67.server.pro',
    'server_user': '40448',
    'server_pass': '7qytnsJShBgo0qlf'
}


class FtpConnection:
    def __init__(self, connection=None):
        ftplib.FTP.maxline = 16384
        if connection is None:
            self.connection = default_connection_settings
        else:
            self.connection = connection
        self.ftp = ftplib.FTP(self.connection['server_name'])
        self.ftp.login(self.connection['server_user'], self.connection['server_pass'])

    def ftp_get_text_file(self, file_path):
        """
        Downloads text file from ftp and returns list of lines
        :param file_path:
        :return:
        """
        lines = []

        def add_to_lines(line):
            lines.append(line)

        self.ftp.retrlines('RETR ' + file_path, add_to_lines)
        return lines

    def ftp_get_json(self, file_path):
        """
        Downloads text file from ftp and returns list of lines
        :param file_path:
        :return:
        """
        self.json_var = ''

        def add_to_lines(line):
            self.json_var += line

        self.ftp.retrlines('RETR ' + file_path, add_to_lines)
        return self.json_var

    def ftp_get_binary_file(self, source_file_path, destination_file_path):
        """
        Downloads binary files
        :param source_file_path:
        :param destination_file_path:
        :return:
        """
        with open(destination_file_path, 'wb') as fp:
            self.ftp.retrbinary('RETR ' + source_file_path, fp.write)

    def ftp_get_dir_files(self, file_path):
        files = []
        self.ftp.cwd(file_path)
        try:
            files = self.ftp.nlst()
        except ftplib.error_perm as resp:
            if str(resp) == "550 No files found":
                print('No files found')
            else:
                raise
        return files


def read_gz_text_file(file_path):
    f = gzip.open(file_path, 'rt')
    file_content = f.read()
    lines = file_content.split('\n')
    f.close()
    return lines


def get_uuid_from_user(user_name):
    class NullNamespace:
        bytes = b''

    return str(uuid.uuid3(NullNamespace, 'OfflinePlayer:Elio'))

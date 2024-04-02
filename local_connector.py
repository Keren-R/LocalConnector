import logging
import os
import shutil
import sys
from typing import List

from base_connector import BaseConnector, AuthenticationStatus

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)-3s | %(name)s | %(message)s', stream=sys.stdout, force=True)


class LocalConnector(BaseConnector):
    """
    This object allows to connect to a local directory in the host and perform file manipulations.
    """

    def connect_to_source(self) -> AuthenticationStatus:
        """
        This function is irrelevant for local implementation.
        :return: AuthenticationStatus
        """
        logging.info("Connected successfully to source")
        return AuthenticationStatus.SUCCEEDED

    def get_connection_details(self) -> dict:
        """
        This function is irrelevant for local implementation.
        :return: dictionary with the connection details.
        """
        logging.info("Using local connector, connection details does not exist.")
        return dict()

    def remove_local_file(self, _id: str) -> bool:
        """
        This function receives a file id and delete it from local directory.
        :param _id: path of the file to delete from local directory.
        :return: True if deletion succeeded, False otherwise.
        """
        res = True
        try:
            os.remove(_id)
        except (FileNotFoundError, PermissionError) as err:
            logging.error(f"An error occurred while trying to delete file {_id}: {err}")
            res = False

        return res

    def download_file(self, remote_path: str, local_path: str) -> bool:
        """
        This function downloads a file from a remote path to a local directory.
        :param remote_path: path to the remote file
        :param local_path: path to the local directory
        :return: True if downloading succeeded, False in case of an error
        """
        res = True
        try:
            shutil.copy(remote_path, local_path)
            logging.info(f"file downloaded successfully from {remote_path} to {local_path}")
        except (shutil.SameFileError, IsADirectoryError, PermissionError, FileNotFoundError) as err:
            logging.error(f"An error occurred while trying to download file {remote_path} to {local_path}: {err}")
            res = False

        return res

    def get_last_modification_time(self, remote_file_path: str) -> float:
        """
        This function returns the last modification time of the addressed file.
        :param remote_file_path:
        :return: the last modification time in timestamp format or 0.0 in case of an error.
        """
        timestamp = float()
        try:
            timestamp = os.path.getmtime(remote_file_path)
        except (FileNotFoundError, OSError) as err:
            logging.error(
                f"an error occurred while trying to get load modification time for file {remote_file_path}: {err}")

        return timestamp

    def get_directory_tree(self, remote_dir: str = ".", include_files: bool = False,
                           include_directories: bool = True) -> List[str]:
        """
        Returns the directory tree in the specified remote directory.
        :param remote_dir: path to the remote directory.
        :param include_files: indicates if files should be displayed.
        :param include_directories: indicates if directories should be displayed.
        :return: the directory tree as a list
        """
        tree_list = []
        for (root, dirs, files) in os.walk(remote_dir, topdown=True):
            tree_list.extend([file for file in files if include_files])
            tree_list.extend([directory for directory in dirs if include_directories])

        return tree_list

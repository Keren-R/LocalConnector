Testing cases for LocalConnector:

testing download_file(self, remote_path: str, local_path: str) -> bool:
1. simple case: remote_path = path to an existing file, local_path = path to the designated directory
2. remote_path = local_path = path to an existing file.
3. remote_path = local_path = path to an existing directory
4. remote_path or local_path does not exist
5. remote path has limited permission

testing get_last_modification_time(self, remote_file_path: str) -> float:
1. simple case: remote_path is an existing file
2. remote_path does not exist

testing get_directory_tree(self, remote_dir: str = ".", include_files: bool = False,
                           include_directories: bool = True) -> List[str]:
1. simple case: remote_dir exist, include_files = True, include_dirs = True
2. remote_dir exist, include_files = False, include_dirs = True
3. remote_dir exist, include_files = True, include_dirs = False
4. remote_dir exist, include_files = False, include_dirs = False
5. remote_dir does not exist

testing remove_local_file(self, _id: str) -> bool:
1. simple case: _id path exist
2. _id path does not exist
3. _id path has limited permission 

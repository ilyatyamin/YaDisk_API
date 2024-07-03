class FileExplorerInterface:
    def __init__(self):
        self._cur_path = None

    # MARK: interface

    def get_folder(self, path):
        raise NotImplementedError

    # MARK: FILES

    def mv(self, src_path, dst_path):
        raise NotImplementedError

    def rm(self, path):
        raise NotImplementedError

    def cp(self, src_path, dst_path):
        raise NotImplementedError

    def isfile(self, path):
        raise NotImplementedError

    # MARK: DIRS

    def isdir(self, path):
        raise NotImplementedError

    def mkdir(self, path):
        raise NotImplementedError

    def rmdir(self, path):
        raise NotImplementedError

    def cd(self, path):
        raise NotImplementedError

    def ls(self, path):
        raise NotImplementedError

    # MARK: supplementary

    def path_conforms(self, path):
        raise NotImplementedError

    def exists(self, path):
        raise NotImplementedError

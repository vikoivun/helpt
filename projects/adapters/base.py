
class Adapter(object):
    def __init__(self, data_source):
        self.data_source = data_source

    def sync_tasks(self, workspace):
        """
        Read tasks for a given workspace.
        """
        raise NotImplementedError()

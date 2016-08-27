
class Adapter(object):
    def __init__(self, data_source):
        self.data_source = data_source

    def read_tasks(self):
        raise NotImplementedError()

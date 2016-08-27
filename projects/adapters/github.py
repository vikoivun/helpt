from .base import Adapter

import requests
import requests_cache

requests_cache.install_cache('github')


class GitHubAdapter(Adapter):
    API_BASE = 'https://api.github.com/'

    def get(self, path):
        headers = {'Authorization': 'token {}'.format(self.token)}
        resp = requests.get(self.API_BASE + path, headers=headers)
        assert resp.status_code == 200
        return resp.json()

    def read_workspaces(self):
        pass

    def read_tasks(self, workspace):
        data = self.get(workspace.origin_id + '/issues')
        from pprint import pprint
        pprint(data)

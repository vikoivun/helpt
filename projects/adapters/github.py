from .base import Adapter
from .sync import ModelSyncher

import requests
import requests_cache

requests_cache.install_cache('github')


class GitHubAdapter(Adapter):
    API_BASE = 'https://api.github.com/'

    def api_get(self, path, **kwargs):
        headers = {'Authorization': 'token {}'.format(self.data_source.token)}
        url = self.API_BASE + path
        objs = []
        while True:
            resp = requests.get(url, headers=headers, params=kwargs)
            assert resp.status_code == 200
            objs += resp.json()
            next_link = resp.links.get('next')
            if not next_link:
                break
            url = next_link['url']

        return objs

    def sync_workspaces(self):
        pass

    def sync_tasks(self, workspace):
        def close_task(task):
            print("Marking %s closed" % task)
            task.set_state('closed')

        data = self.api_get('repos/{}/issues'.format(workspace.origin_id))

        data_source_users = self.data_source.data_source_users.all()
        users_by_id = {int(u.origin_id): u.user for u in data_source_users}

        Task = workspace.tasks.model

        syncher = ModelSyncher(workspace.tasks.open(),
                               lambda task: int(task.origin_id),
                               delete_func=close_task)
        for task in data:
            obj = syncher.get(task['number'])
            if not obj:
                obj = Task(workspace=workspace, origin_id=task['number'])

            obj.name = task['title']
            for f in ['created_at', 'updated_at', 'closed_at']:
                setattr(obj, f, task[f])

            assert task['state'] == 'open'
            obj.state = 'open'

            syncher.mark(obj)
            obj.save()

            assignees = task['assignees']
            new_assignees = set()
            for assignee in assignees:
                user = users_by_id.get(assignee['id'])
                if not user:
                    continue
                new_assignees.add(user)
            old_assignees = set([x.user for x in obj.assignments.all()])

            for user in new_assignees - old_assignees:
                obj.assignments.create(user=user)
            remove_assignees = old_assignees - new_assignees
            if remove_assignees:
                obj.assignments.filter(user__in=remove_assignees)

            print('#{}: [{}] {}'.format(task['number'], task['state'], task['title']))

        syncher.finish()

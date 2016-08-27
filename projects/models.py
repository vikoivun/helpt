from django.conf import settings
from django.db import models

from .adapters import GitHubAdapter


class DataSource(models.Model):
    TYPES = (
        ('github', 'GitHub'),
    )

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def adapter(self):
        if not hasattr(self, '_adapter'):
            if self.type == 'github':
                self._adapter = GitHubAdapter(self.githubdatasource)
            else:
                raise NotImplementedError('Unknown data source type: {}'.format(self.type))
        return self._adapter

    def __str__(self):
        return self.name


class GitHubDataSource(DataSource):
    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)
    token = models.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        self.type = 'github'
        super().__init__(*args, **kwargs)


class DataSourceUser(models.Model):
    data_source = models.ForeignKey(DataSource, db_index=True,
                                    related_name='users')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True,
                             related_name='data_sources')
    origin_id = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return "{}: {} as {}".format(self.data_source, self.user, self.origin_id)


class Project(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProjectUser(models.Model):
    project = models.ForeignKey(Project, db_index=True, related_name='users')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True,
                             related_name='projects')

    def __str__(self):
        return "{} on {}".format(self.user, self.project)


class Workspace(models.Model):
    data_source = models.ForeignKey(DataSource, db_index=True,
                                    related_name='workspaces')
    project = models.ForeignKey(Project, db_index=True,
                                related_name='workspaces')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    origin_id = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def read_tasks(self):
        adapter = self.data_source.adapter
        adapter.read_tasks(self)


class Task(models.Model):
    STATE_OPEN = 'open'
    STATE_CLOSED = 'closed'

    STATES = (
        (STATE_OPEN, 'open'),
        (STATE_CLOSED, 'closed')
    )

    name = models.CharField(max_length=100)
    workspace = models.ForeignKey(Workspace, db_index=True, related_name='tasks')
    origin_id = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=10, choices=STATES, db_index=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.workspace)


class TaskAssignment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_tasks',
                             db_index=True)
    task = models.ForeignKey(Task, related_name='assigned_users', db_index=True)

    def __str__(self):
        return "{} assigned to {}".format(self.task, self.user)

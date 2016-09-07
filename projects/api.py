from dynamic_rest import serializers, viewsets
from .models import Task, Workspace, Project
from users.api import UserSerializer


all_views = []


def register_view(klass, name=None, base_name=None):
    if not name:
        name = klass.serializer_class.Meta.name

    entry = {'class': klass, 'name': name}
    if base_name is not None:
        entry['base_name'] = base_name
    all_views.append(entry)

    return klass


class ProjectSerializer(serializers.DynamicModelSerializer):
    class Meta:
        model = Project
        name = 'project'
        plural_name = 'project'


@register_view
class ProjectViewSet(viewsets.DynamicModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class WorkspaceSerializer(serializers.DynamicModelSerializer):
    class Meta:
        model = Workspace
        name = 'workspace'
        plural_name = 'workspace'


@register_view
class WorkspaceViewSet(viewsets.DynamicModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer


class TaskSerializer(serializers.DynamicModelSerializer):
    workspace = serializers.DynamicRelationField(WorkspaceSerializer)
    assigned_users = serializers.DynamicRelationField(UserSerializer, many=True)

    class Meta:
        model = Task
        name = 'task'
        plural_name = 'task'

@register_view
class TaskViewSet(viewsets.DynamicModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

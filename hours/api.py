from dynamic_rest import serializers, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import DjangoObjectPermissions
from .models import Entry
from users.api import UserSerializer
import rules
import logging
from django.contrib.auth import get_user_model

all_views = []

logger = logging.getLogger(__name__)

def register_view(klass, name=None, base_name=None):
    if not name:
        name = klass.serializer_class.Meta.name

    entry = {'class': klass, 'name': name}
    if base_name is not None:
        entry['base_name'] = base_name
    all_views.append(entry)

    return klass


class EntrySerializer(serializers.DynamicModelSerializer):
    user = serializers.DynamicRelationField(UserSerializer)

    class Meta:
        model = Entry
        name = 'entry'
        plural_name = 'entry'


@register_view
class EntryViewSet(viewsets.DynamicModelViewSet):
    permission_classes = (DjangoObjectPermissions,)
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


@rules.predicate
def is_entry_creator(user, entry):
    print("Checking change_entry")
    return user == entry.user


@rules.predicate
def is_task_assignee(user, entry):
    if entry is None:
        print("No entry, allowing")
        return True

    import traceback
    traceback.print_stack()

    User = get_user_model()

    assignees = User.objects.filter(id__in=entry.task.assigned_users.values("user_id"))
    response = user in assignees

    print("Returning response: {}".format(response))
    return response

rules.add_perm('hours.add_entry', is_task_assignee)
rules.add_perm('hours.change_entry', is_entry_creator)

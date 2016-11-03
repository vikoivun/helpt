from dynamic_rest import serializers, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Entry
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


class EntrySerializer(serializers.DynamicModelSerializer):
    user = serializers.DynamicRelationField(UserSerializer)

    class Meta:
        model = Entry
        name = 'entry'
        plural_name = 'entry'

@register_view
@permission_classes((IsAuthenticated, ))
class EntryViewSet(viewsets.DynamicModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

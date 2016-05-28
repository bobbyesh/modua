from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .models import Definitions
from .serializers import DefinitionSerializer


class Search(APIView):

    renderer_classes = (JSONRenderer,)

    def get(self, request, format=None):
        definitions = Definitions.objects.all()
        serializer = DefinitionSerializer(definitions, many=True)
        return Response(serializer.data)

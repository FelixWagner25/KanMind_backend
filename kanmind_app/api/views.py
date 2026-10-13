from rest_framework import viewsets
from kanmind_app.models import Board
from .serializers import BoardSerializer


class BoardViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing board instances.
    """
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

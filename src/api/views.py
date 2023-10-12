from rest_framework import (viewsets, permissions)
from django.contrib.auth import get_user_model
from appeals.models import (Appeal, Category)
from .serializers import (AppealSerializer, AppealListSerializer, CategorySerializer, UserSerializer)
from rest_framework.response import Response
from .permissions import IsCreatorOrReadOnly


class AppealViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows appeals to be viewed or edited.
    """
    queryset = Appeal.objects.all()
    serializer_class = AppealSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = [IsCreatorOrReadOnly]


    def list(self, request, *args, **kwargs):
        appeals = Appeal.objects.all()
        context = {'request': request}
        self.serializer_class = AppealListSerializer
        serializer = AppealListSerializer(appeals, many=True, context=context)

        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)        

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns the Category list or the requested one
    """
    queryset = Category.objects.prefetch_related('appeals')
    serializer_class = CategorySerializer
    http_method_names = ['get']

class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    model = get_user_model()
    queryset = model.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = [permissions.IsAdminUser]
    
    
    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)
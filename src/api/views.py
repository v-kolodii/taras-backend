from rest_framework import (viewsets, permissions)
from django.contrib.auth import get_user_model
from appeals.models import (Appeal, Category, AppealStatus)
from .serializers import (AppealSerializer, AppealListSerializer, CategorySerializer, UserSerializer, UserListSerializer)
from rest_framework.response import Response
from .permissions import IsCreatorOrReadOnly
from django.db.models import Prefetch
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class AppealViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows appeals to be viewed or edited.
    """
    queryset = Appeal.objects.all() 
    serializer_class = AppealSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = [IsCreatorOrReadOnly]


    def list(self, request, *args, **kwargs):
        appeals = Appeal.objects.filter(app_status = AppealStatus.POSTED)
        context = {'request': request}
        self.serializer_class = AppealListSerializer
        serializer = AppealListSerializer(appeals, many=True, context=context)

        return Response(serializer.data)
    
    # def perform_create(self, serializer):
    #     serializer.save(creator = self.request.user)

    def create(self, request, *args, **kwargs):
        instance = request.data
        category = get_object_or_404(Category, pk=int(instance['category']))
        new_appeal = Appeal.objects.create(title=instance['title'],
                                           text=instance['text'],
                                           app_status=AppealStatus.POSTED,
                                           category=category,
                                           creator = self.request.user
                                           )
        new_appeal.save()
        context = {'request': request}
        serializer = AppealListSerializer(new_appeal, context=context)

        return Response(serializer.data)

    @action(detail=True, methods=['patch'], name='assign to me')
    def assign(self, request, pk=None):
        """Update the assigned_to appeal"""   
        self.permission_classes = [permissions.IsAuthenticated]
        serializer = self.get_serializer
        serializer.save(assigned_to = request.user)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns the Category list or the requested one
    """
    queryset = Category.objects.prefetch_related(Prefetch('appeals', Appeal.objects.filter(app_status = AppealStatus.POSTED)))
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

    def list(self, request, *args, **kwargs):
        users = self.model.objects.all()
        context = {'request': request}
        self.serializer_class = UserListSerializer
        serializer = UserListSerializer(users, many=True, context=context)

        return Response(serializer.data)
    
    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)
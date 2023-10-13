from django.urls import path
from rest_framework import (routers, urlpatterns as up)
from .views import (AppealViewSet, CategoryViewSet, UserViewSet)


# add different urls:
# appeal_list = AppealViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })

# appeal_detail = AppealViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy',
# })

# urlpatterns = [
#     path('appeals/', appeal_list, name='appeals-list'),
#     path('appeals/<int:pk>/', appeal_detail, name='appeal-detail'),
# ]

# urlpatterns = up.format_suffix_patterns(urlpatterns)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'appeals', AppealViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = router.urls

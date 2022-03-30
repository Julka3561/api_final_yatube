from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, GroupViewSet, FollowViewSet, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comment')
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]

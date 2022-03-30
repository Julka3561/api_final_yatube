from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from api.serializers import (CommentSerializer, GroupSerializer,
                             FollowSerializer, PostSerializer)
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """API для работы с постами. Список постов, публикация нового, детали поста,
    редактирование и удаление."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """API для работы с группами. Список групп, детали группы."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """API для работы с комментариями. Список комментариев, публикация нового,
    детали комментария, редактирование и удаление."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """API для работы с подписками. Список авторов, на которых подписан
    пользователь, подписка на новых авторов"""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from django.urls import path
from app import views
from app.views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, AnswerSubmit, CommentSubmit, UpvoteSubmit, TagList, PostTypeList, CommentLike, Subscribers

app_name = 'app'

urlpatterns = [
    path('', PostList.as_view(), name='index'),
    path('<int:pk>/<slug:slug>', PostDetail.as_view(), name="view-post"),
    path('add/', PostCreate.as_view(), name='add-post'),
    path('edit/<int:pk>', PostUpdate.as_view(), name='edit-post'),
    path('delete/<int:pk>', PostDelete.as_view(), name='delete-post'),
    path('answer/<int:pk>/post', AnswerSubmit.as_view(), name="post-answer"),
    path('comment/<int:pk>/post', CommentSubmit.as_view(), name="post-comment"),
    path('answer/<int:pk>/upvote', UpvoteSubmit.as_view(), name="add-upvote"),
    path('tags/<slug:slug>', TagList.as_view(), name="tag-list"),
    path('type/<slug:slug>', PostTypeList.as_view(), name="post-type-list"),
    path('comment/<int:pk>/like', CommentLike.as_view(), name="comment-like"),
    path('subscribe/<int:pk>/add', Subscribers.as_view(), name="subscribe-add"),
]

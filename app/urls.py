from django.urls import path
from app import views
from app.views import PostStart, PostList, PostDetail, PostUpdateQuestion, PostUpdateExperience, PostDelete, AnswerSubmit, CommentSubmit, UpvoteSubmit, TagList, PostTypeList, CommentLike, Subscribers, FlagPost, PostCreateExperience, PostCreateQuestion

app_name = 'app'

urlpatterns = [
    path('', PostList.as_view(), name='index'),
    path('start', PostStart.as_view(), name='start'),
    path('<int:pk>/edit/question', PostUpdateQuestion.as_view(), name='edit-post'),
    path('<int:pk>/edit/experience', PostUpdateExperience.as_view(), name='edit-experience'),
    path('<int:pk>/delete', PostDelete.as_view(), name='delete-post'),
    path('<int:pk>/flag', FlagPost.as_view(), name='flag-post'),
    path('<int:pk>/<slug:slug>', PostDetail.as_view(), name="view-post"),
    path('add/experience', PostCreateExperience.as_view(), name='add-post-experience'),
    path('add/question', PostCreateQuestion.as_view(), name='add-post-question'),
    path('answer/<int:pk>/post', AnswerSubmit.as_view(), name="post-answer"),
    path('comment/<int:pk>/post', CommentSubmit.as_view(), name="post-comment"),
    path('answer/<int:pk>/upvote', UpvoteSubmit.as_view(), name="add-upvote"),
    path('tags/<slug:slug>', TagList.as_view(), name="tag-list"),
    path('type/<slug:slug>', PostTypeList.as_view(), name="post-type-list"),
    path('comment/<int:pk>/like', CommentLike.as_view(), name="comment-like"),
    path('subscribe/<int:pk>/add', Subscribers.as_view(), name="subscribe-add"),
]

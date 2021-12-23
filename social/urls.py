from django.urls import path
from social.views import (
    tweet_page,
    PostListView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    CommentUpdateView,
    CommentDeleteView,
    AddFollowView,
    RemoveFollowView,
    AddLikeView,
    AddDislikeView,
    UserFollowersView,
    CommentLikeView,
    CommentDislikeView,
    CommentReplyView,
    PostNotificationsView,
    FollowNotificationsView,
    ListThreadsView,
    CreateThreadView,
    ThreadView,
    CreateMessageView,
    ThreadNotificationView
)

urlpatterns = [
    path('', PostListView.as_view(), name="home_page"),
    path('tweet', tweet_page, name="tweet_page"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post_detail"),

    path('post/<int:pk>/like/', AddLikeView.as_view(), name="post_like"),
    path('post/<int:pk>/dislike/', AddDislikeView.as_view(), name="post_dislike"),

    path('post/update/<int:pk>/', PostUpdateView.as_view(), name="post_update"),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name="post_delete"),

    path('post/<int:post_pk>/comment_update/<int:pk>/', CommentUpdateView.as_view(), name="comment_update"),
    path('post/<int:post_pk>/comment_delete/<int:pk>/', CommentDeleteView.as_view(), name="comment_delete"),

    path('post/<int:post_pk>/comment/<int:pk>/like/', CommentLikeView.as_view(), name="comment_like"),
    path('post/<int:post_pk>/comment/<int:pk>/dislike/', CommentDislikeView.as_view(), name="comment_dislike"),

    path('post/<int:post_pk>/comment/<int:pk>/reply/', CommentReplyView.as_view(), name="comment_reply"),

    path('profile/<int:pk>/followers/', UserFollowersView.as_view(), name="user_followers"),
    path('profile/<int:pk>/followers/add/', AddFollowView.as_view(), name="add_follow"),
    path('profile/<int:pk>/followers/remove/', RemoveFollowView.as_view(), name="remove_follow"),


    path(
        'notification/<int:notification_pk>/post/<int:post_pk>/',
        PostNotificationsView.as_view(),
        name="post_notification"
    ),

    path(
        'notification/<int:notification_pk>/post/<int:post_pk>/',
        FollowNotificationsView.as_view(),
        name="follow_notification"
    ),

    path(
        'notification/<int:notification_pk>/thread/<int:thread_pk>/',
        ThreadNotificationView.as_view(),
        name="thread_notification"
    ),

    path('inbox/', ListThreadsView.as_view(), name="inbox"),
    path('inbox/create_thread/', CreateThreadView.as_view(), name="create_thread"),
    path('inbox/<int:pk>/', ThreadView.as_view(), name="thread"),
    path('inbox/<int:pk>/create_message/', CreateMessageView.as_view(), name="create_message"),
]




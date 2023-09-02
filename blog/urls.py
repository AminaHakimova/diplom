from django.urls import path

from blog.views import (
    PostListView,
    PostDetailView,
    CommentsCreateView,
    LikeCreateView,
    logout_user,
    UserRegisterView,
    PostFilterView,
    UserLoginView,
    PostCreateView,
    UserView,
    PostUserFilterView
)

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path('user/', UserView.as_view(), name="user"),
    path('user/login/', UserLoginView.as_view(), name="login"),
    path('user/register/', UserRegisterView.as_view(), name="register"),
    path('user/logout/', logout_user, name="logout"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("posts/", PostFilterView.as_view(), name="filter"),
    path('posts/create/', PostCreateView.as_view(), name="create"),
    path("user/posts/", PostUserFilterView.as_view(), name="user_filter"),

    path("posts/<int:pk>/comments/", CommentsCreateView.as_view(),
         name="comments"),

    path("posts/<int:pk>/likes/", LikeCreateView.as_view(),
         name="likes"),
]

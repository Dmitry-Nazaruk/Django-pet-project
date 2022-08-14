from django.urls import path


from vote_app.views import Main_html, RegisterFormView, LoginFormView, LogoutView, Create_Post, All_post_main, \
    PostDetail, Create_comment, Change_User, Profile

urlpatterns = [
    path('', Main_html.as_view(), name='home'),
    path('reg/', RegisterFormView.as_view(), name='reg'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create_post/', Create_Post.as_view(), name='create_post'),
    path('posts/', All_post_main.as_view(), name='all_posts' ),
   # path('posts/<int:pk>/', postdetail),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('posts/<int:pk>/create_comment', Create_comment.as_view(), name='create_comment'),
    path('profile', Profile.as_view(), name='profile'),
    path('profile/change', Change_User.as_view(), name='profile_change'),
]
from django.urls import path,include
from .views import *
import debug_toolbar
from django.views.decorators.cache import cache_page

urlpatterns=[
    # path('',index,name='home'),
    path('logout',user_logout,name='logout'),
    path('register/',register,name='register'),
    path('login/',user_login,name='login'),
    # path('',cache_page(60)(HomeNews.as_view()),name='home'),
    path('',HomeNews.as_view(),name='home'),
    path('category/<int:category_id>/',Categories.as_view(),name='category'),
    path('posts/<int:pk>/',get_post,name='post'),
    path('posts/new_post/',new_post.as_view(),name='new_post'),

]



urlpatterns += [ path('__debug__/', include(debug_toolbar.urls)),]
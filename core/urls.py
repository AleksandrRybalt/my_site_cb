from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rate', views.RateView.as_view(), name='rate'),
    path('bik', views.BikView.as_view(), name='bik'),
    path('currency_dynamic', views.CurrencyDynamic.as_view(), name='currency_dynamic'),
    path('precious_metals', views.PreciousMetals.as_view(), name='precious_metals'),
    path('registration', views.RegisterUser.as_view(), name='registration_page'),
    path('authorization', views.LoginUser.as_view(), name='auth_page'),
    path('logout', views.logout_user, name='logout'),

    path('posts', views.Posts.as_view(), name='posts'),
    path('add_post', views.AddPost.as_view(), name='add_post'),
    path('posts/<slug:post_slug>', views.Post.as_view(), name='post'),
    path('category/<slug:category_slug>', views.Category.as_view(), name='category'),
]

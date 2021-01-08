from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("<int:num>", views.listing, name="listing"),
    path("<int:num>/wish/", views.wish, name="wish"),
    path("<int:num>/bid/", views.bid, name="bid"),
    path("<int:num>/close/", views.close, name="close"),
    path("watchlist/<str:name>/", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:title>/", views.category, name="category")
]

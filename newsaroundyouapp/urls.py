from django.urls import path
from . import views

app_name = "newsaroundyouapp"
urlpatterns = [
    path("", views.home, name="home"),
    path(
        "category/<str:category>/", views.search_by_category, name="search_by_category"
    ),
    path("search", views.search, name="search"),
    path("error", views.error_page, name="error"),
]

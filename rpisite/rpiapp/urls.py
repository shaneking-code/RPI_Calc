from django.urls import path
from . import views

app_name = "rpiapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:season_id>/games/", views.season_results, name="season results"),
    path("<int:season_id>/", views.season_detail, name="season detail")
]
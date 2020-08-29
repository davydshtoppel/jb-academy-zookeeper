from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import MainView, AllNewsView, NewsView, CreateNewsView


urlpatterns = [
    path("", MainView.as_view()),
    path("news/", AllNewsView.as_view()),
    path("news/create/", CreateNewsView.as_view()),
    path("news/<int:news_id>/", NewsView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from .views import GenerateScheduleView, SaveScheduleView, index

urlpatterns = [
    # path('', index, name='index'),
    path('api/generate-schedule/', GenerateScheduleView.as_view(), name='generate-schedule'),
    path('api/save-schedule/', SaveScheduleView.as_view(), name='save-schedule'),
]

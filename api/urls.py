from django.urls import path
from . import views

urlpatterns = [
    path('', view = views.index , name='login'),
    path('token/', view = views.get_access_token, name='access_token'),
]
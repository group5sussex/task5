from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
from . import views3d
from . import solver3d


urlpatterns = [
    path("index", views.index, name="index"),
    path("submit/", views.submit, name="submit"),
    path("3d/submit/", solver3d.submit, name="3dsubmit"),

    #path("3d/submit/", views3d.submit, name="3dsubmit"),
]
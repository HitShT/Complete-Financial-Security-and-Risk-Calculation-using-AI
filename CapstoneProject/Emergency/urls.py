from django.conf.urls import url,include
from django.contrib import admin
from Emergency import views

app_name = "Emergency"

urlpatterns = [
    url(r"^test/$",views.test),

]

from django.urls import path

from .frontend_views import index

app_name = "frontend"

urlpatterns = [
    path("", index, name="home"),
    path("dealers", index, name="dealers"),
    path("dealers/<str:state>", index, name="dealers_by_state"),
    path("dealer/<int:dealer_id>", index, name="dealer"),
    path("postreview/<int:dealer_id>", index, name="postreview"),
    path("login", index, name="login_page"),
    path("register", index, name="register_page"),
]

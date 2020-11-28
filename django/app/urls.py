from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="homepage"),
    #path("?id=<int:id>/", views.index, name="homepage"),
    #path("?name=<str:name>/", views.index, name="homepage"),
    #path("?id=<int:id>&name=<str:name>/", views.index, name="homepage"),

    path("create",views.create,name="create student"),
    path("create/submit/",views.create_submit,name="create submit"),
    path("delete?id=<int:id>/",views.delete,name="delete student"),
    path("update?id=<int:id>/",views.update,name="update student"),
    path("update?id=<int:id>/submit/",views.update_submit,name="update submit"),
    path("create/upload/",views.upload,name="upload photo while creating"),
    path("update/upload/",views.upload,name="upload photo while updating"),
]

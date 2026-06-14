from django.urls import path
from .views import EmployeeCreateView, EmployeeListView, EmployeeDetailView, UploadProfilePictureView, EmployeeDeleteView

urlpatterns = [
    path("create/", EmployeeCreateView.as_view(), name="create_employee"),
    path('/', EmployeeListView.as_view(), name='alL-employee'),
    path("<int:id>/", EmployeeDetailView.as_view(), name="employee-detail"),
    path(
    "profile-picture/",
    UploadProfilePictureView.as_view(),
    name="upload-profile-picture"
    ),
    path(
    "delete/<int:id>/",
    EmployeeDeleteView.as_view(),
    name="del_employee"
)
]
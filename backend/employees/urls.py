from django.urls import path
from .views import EmployeeCreateView, EmployeeListView, EmployeeDetailView, UploadProfilePictureView, EmployeeDeleteView, ChangePasswordView,EmployeeUpdateView
urlpatterns = [
    path("create/", EmployeeCreateView.as_view(), name="create_employee"),
    path('all/', EmployeeListView.as_view(), name='alL-employee'),
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
),
    path(
    "reset_password/",
    ChangePasswordView.as_view(),
    name="reset_password"
),

path(
    "update/<int:id>/",
    EmployeeUpdateView.as_view(),
    name='update_employee'
)


]
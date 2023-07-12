from django.urls import path
from .views import *

urlpatterns = [
    path("customers/", CustomerListAPIView.as_view()),
    path("export/<str:src>/", export_source_data),
    path("exported_files/", ExportedFilesListAPIView.as_view())
]

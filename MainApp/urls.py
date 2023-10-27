from django.urls import path
from . import views

urlpatterns = [
    path('import-csv/',views.csv_importer,name="import-csv"),
]

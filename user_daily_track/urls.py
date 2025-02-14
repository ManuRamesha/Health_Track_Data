# these are the django imports
from django.urls import path

# these are local imports
from .views import DailyTrackViewCRUDView, DownloadMonthlyReportAPIView

urlpatterns = [
    path('', DailyTrackViewCRUDView.as_view(), name='daily_track_crud_view'),
    path('download/<int:year>/<int:month>', DownloadMonthlyReportAPIView.as_view(), name='download_monthly_report')
]
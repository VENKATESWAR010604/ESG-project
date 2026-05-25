from django.urls import path
from .views import (
    SapIngestView,
    UtilityIngestView,
    TravelIngestView,
    ReviewRowsView,
    SummaryView,
    AuditLogView,
    ApproveRowView,
    RejectRowView,
    DeleteRowView,
)

urlpatterns = [
    path("ingest/sap/", SapIngestView.as_view()),
    path("ingest/utility/", UtilityIngestView.as_view()),
    path("ingest/travel/", TravelIngestView.as_view()),

    path("review/rows/", ReviewRowsView.as_view()),
    path("review/summary/", SummaryView.as_view()),
    path("audit/logs/", AuditLogView.as_view()),

    path("review/rows/<int:row_id>/approve/", ApproveRowView.as_view()),
    path("review/rows/<int:row_id>/reject/", RejectRowView.as_view()),
    path("review/rows/<int:row_id>/delete/", DeleteRowView.as_view()),
]
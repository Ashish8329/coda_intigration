from django.urls import path
from scanner.views import (
    AlertListView,
    DocumentListView,
    resolve_alert,
    remediate_delete_page,
    alerts_dashboard,
    documents_dashboard
)

urlpatterns = [
    path("alerts/", AlertListView.as_view(), name="alerts"),
    path("documents/", DocumentListView.as_view(), name="documents"),
    path("dashboard/alerts/", alerts_dashboard, name="alert_list"),
    path("dashboard/documents/", documents_dashboard, name="document_list"),


    # Remediation endpoints
    path("alerts/<int:pk>/resolve/", resolve_alert, name="resolve-alert"),
    path("documents/<str:doc_id>/pages/<str:page_id>/delete/",
         remediate_delete_page,
         name="delete-page"),
]

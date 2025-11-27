from django.urls import path
from scanner.views import (
    AlertListView,
    DocumentListView,
    resolve_alert,
    remediate_delete_page,
)

urlpatterns = [
    path("alerts/", AlertListView.as_view(), name="alerts"),
    path("documents/", DocumentListView.as_view(), name="documents"),

    # Remediation endpoints
    path("alerts/<int:pk>/resolve/", resolve_alert, name="resolve-alert"),
    path("documents/<str:doc_id>/pages/<str:page_id>/delete/",
         remediate_delete_page,
         name="delete-page"),
]

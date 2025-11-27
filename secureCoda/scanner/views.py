from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from scanner.models import Alert, Document
from scanner.serializers import AlertSerializer, DocumentSerializer
from scanner.coda_client import CodaClient


class AlertListView(generics.ListAPIView):
    """
    Returns all active (unresolved) alerts.
    """
    queryset = Alert.objects.filter(resolved=False).order_by("-created_at")
    serializer_class = AlertSerializer


class DocumentListView(generics.ListAPIView):
    """
    Returns list of synced Coda documents.
    """
    queryset = Document.objects.all().order_by("name")
    serializer_class = DocumentSerializer


@api_view(["POST"])
def resolve_alert(request, pk):
    """
    Mark an alert as resolved (does NOT modify Coda).
    """
    try:
        alert = Alert.objects.get(pk=pk)
        alert.resolved = True
        alert.save()
    except Alert.DoesNotExist:
        return Response({"error": "Alert not found"}, status=404)

    return Response({"message": "Alert resolved"}, status=200)


@api_view(["POST"])
def remediate_delete_page(request, doc_id, page_id):
    """
    Deletes a Coda page (remediation action).
    """
    client = CodaClient()

    try:
        client.delete_page(doc_id, page_id)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    return Response({"message": "Page deleted successfully"}, status=200)



def alerts_dashboard(request):
    return render(request, "dashboard/alerts.html")

def documents_dashboard(request):
    return render(request, "dashboard/documents.html")

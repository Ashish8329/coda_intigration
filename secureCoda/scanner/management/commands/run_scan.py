from django.core.management.base import BaseCommand
from scanner.services.scan_runner import ScanRunner


class Command(BaseCommand):
    help = "Runs the full Coda security scan"

    def handle(self, *args, **options):
        scan = ScanRunner()
        scan.run_scan()
        self.stdout.write(self.style.SUCCESS("Scan completed successfully."))

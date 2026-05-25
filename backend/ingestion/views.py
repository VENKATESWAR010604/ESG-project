from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
import csv
import io
import os
import json

from .models import IngestionBatch, ActivityRow, AuditLog
from .serializers import ActivityRowSerializer


def parse_float(value):
    try:
        if value is None:
            return None
        value = str(value).strip()
        if value == "":
            return None
        return float(value)
    except:
        return None


class SapIngestView(APIView):
    def post(self, request):
        file_path = os.path.join("sample_data", "sap_fuel_procurement.csv")

        with open(file_path, "r", encoding="utf-8") as f:
            decoded_file = f.read()

        # IMPORTANT: Your SAP file is tab-separated
        reader = csv.DictReader(io.StringIO(decoded_file), delimiter="\t")

        batch = IngestionBatch.objects.create(
            source_type="SAP",
            file_name="sap_fuel_procurement.csv"
        )

        total = failed = suspicious = 0

        for row in reader:
            total += 1

            quantity = parse_float(row.get("Menge"))
            unit = row.get("Einheit")
            plant_code = row.get("Werk")
            material = row.get("Material")

            status_value = "PENDING"
            error_reason = None
            suspicious_reason = None

            if quantity is None:
                status_value = "FAILED"
                error_reason = "Invalid quantity"
                failed += 1

            elif not plant_code:
                status_value = "FAILED"
                error_reason = "Missing plant code"
                failed += 1

            elif plant_code == "9999":
                status_value = "SUSPICIOUS"
                suspicious_reason = "Unknown SAP plant code"
                suspicious += 1

            elif quantity > 10000:
                status_value = "SUSPICIOUS"
                suspicious_reason = "Unusually high fuel/procurement quantity"
                suspicious += 1

            normalized = {
                "plant_code": plant_code,
                "material": material,
                "quantity": quantity,
                "unit": unit,
                "posting_date": row.get("Buchungsdatum"),
                "vendor": row.get("Lieferant"),
                "cost_center": row.get("Kostenstelle"),
            }

            ActivityRow.objects.create(
                batch=batch,
                source_type="SAP",
                raw_data=row,
                normalized_data=normalized,
                scope="SCOPE_1",
                activity_type="fuel_procurement",
                quantity=quantity,
                unit=unit,
                status=status_value,
                error_reason=error_reason,
                suspicious_reason=suspicious_reason,
            )

        batch.total_rows = total
        batch.failed_rows = failed
        batch.suspicious_rows = suspicious
        batch.save()

        return Response({
            "message": "SAP data ingested from sample file",
            "batch_id": batch.id,
            "total_rows": total,
            "failed_rows": failed,
            "suspicious_rows": suspicious
        })


class UtilityIngestView(APIView):
    def post(self, request):
        file_path = os.path.join("sample_data", "utility_electricity.csv")

        with open(file_path, "r", encoding="utf-8") as f:
            decoded_file = f.read()

        reader = csv.DictReader(io.StringIO(decoded_file))

        batch = IngestionBatch.objects.create(
            source_type="UTILITY",
            file_name="utility_electricity.csv"
        )

        total = failed = suspicious = 0

        for row in reader:
            total += 1

            usage = parse_float(row.get("Usage"))
            unit = row.get("Unit")

            status_value = "PENDING"
            error_reason = None
            suspicious_reason = None

            if usage is None:
                status_value = "FAILED"
                error_reason = "Invalid electricity usage"
                failed += 1

            elif usage > 5000:
                status_value = "SUSPICIOUS"
                suspicious_reason = "Unusually high electricity usage"
                suspicious += 1

            normalized = {
                "account_number": row.get("AccountNumber"),
                "meter_number": row.get("MeterNumber"),
                "service_start": row.get("ServiceStart"),
                "service_end": row.get("ServiceEnd"),
                "usage": usage,
                "unit": unit,
                "tariff": row.get("Tariff"),
                "total_amount": row.get("TotalAmount"),
            }

            ActivityRow.objects.create(
                batch=batch,
                source_type="UTILITY",
                raw_data=row,
                normalized_data=normalized,
                scope="SCOPE_2",
                activity_type="electricity",
                quantity=usage,
                unit=unit,
                status=status_value,
                error_reason=error_reason,
                suspicious_reason=suspicious_reason,
            )

        batch.total_rows = total
        batch.failed_rows = failed
        batch.suspicious_rows = suspicious
        batch.save()

        return Response({
            "message": "Utility data ingested from sample file",
            "batch_id": batch.id,
            "total_rows": total,
            "failed_rows": failed,
            "suspicious_rows": suspicious
        })


class TravelIngestView(APIView):
    def post(self, request):
        file_path = os.path.join("sample_data", "travel_data.json")

        with open(file_path, "r", encoding="utf-8") as f:
            records = json.load(f)

        batch = IngestionBatch.objects.create(
            source_type="TRAVEL",
            file_name="travel_data.json"
        )

        total = failed = suspicious = 0

        for row in records:
            total += 1

            category = row.get("category")
            distance = parse_float(row.get("distance_km"))
            nights = parse_float(row.get("nights"))

            status_value = "PENDING"
            error_reason = None
            suspicious_reason = None
            quantity = distance or nights

            if category == "flight" and distance is None:
                status_value = "FAILED"
                error_reason = "Flight distance missing"
                failed += 1

            elif category == "ground_transport" and distance and distance > 500:
                status_value = "SUSPICIOUS"
                suspicious_reason = "Unusually high ground transport distance"
                suspicious += 1

            normalized = {
                "employee_id": row.get("employee_id"),
                "category": category,
                "origin": row.get("origin"),
                "destination": row.get("destination"),
                "city": row.get("city"),
                "distance_km": distance,
                "nights": nights,
                "travel_date": row.get("travel_date"),
                "amount": row.get("amount"),
            }

            ActivityRow.objects.create(
                batch=batch,
                source_type="TRAVEL",
                raw_data=row,
                normalized_data=normalized,
                scope="SCOPE_3",
                activity_type=category,
                quantity=quantity,
                unit="km" if distance else "nights",
                status=status_value,
                error_reason=error_reason,
                suspicious_reason=suspicious_reason,
            )

        batch.total_rows = total
        batch.failed_rows = failed
        batch.suspicious_rows = suspicious
        batch.save()

        return Response({
            "message": "Travel data ingested from sample file",
            "batch_id": batch.id,
            "total_rows": total,
            "failed_rows": failed,
            "suspicious_rows": suspicious
        })


class ReviewRowsView(APIView):
    def get(self, request):
        rows = ActivityRow.objects.all().order_by("-created_at")

        status_filter = request.GET.get("status")
        source_filter = request.GET.get("source")
        scope_filter = request.GET.get("scope")

        if status_filter:
            rows = rows.filter(status=status_filter.upper())

        if source_filter:
            rows = rows.filter(source_type=source_filter.upper())

        if scope_filter:
            rows = rows.filter(scope=scope_filter.upper())

        serializer = ActivityRowSerializer(rows, many=True)
        return Response(serializer.data)


class AuditLogView(APIView):
    def get(self, request):
        logs = AuditLog.objects.all().order_by("-created_at")

        data = []
        for log in logs:
            data.append({
                "id": log.id,
                "row_id": log.row.id,
                "action": log.action,
                "note": log.note,
                "created_at": log.created_at,
            })

        return Response(data)


class SummaryView(APIView):
    def get(self, request):
        return Response({
            "total_rows": ActivityRow.objects.count(),
            "pending_rows": ActivityRow.objects.filter(status="PENDING").count(),
            "failed_rows": ActivityRow.objects.filter(status="FAILED").count(),
            "suspicious_rows": ActivityRow.objects.filter(status="SUSPICIOUS").count(),
            "approved_rows": ActivityRow.objects.filter(status="APPROVED").count(),
            "rejected_rows": ActivityRow.objects.filter(status="REJECTED").count(),
            "sap_rows": ActivityRow.objects.filter(source_type="SAP").count(),
            "utility_rows": ActivityRow.objects.filter(source_type="UTILITY").count(),
            "travel_rows": ActivityRow.objects.filter(source_type="TRAVEL").count(),
        })


class ApproveRowView(APIView):
    def post(self, request, row_id):
        row = ActivityRow.objects.get(id=row_id)

        if row.status == "FAILED":
            return Response(
                {"error": "Failed rows cannot be approved"},
                status=400
            )

        row.status = "APPROVED"
        row.is_locked = True
        row.approved_at = timezone.now()
        row.save()

        AuditLog.objects.create(
            row=row,
            action="APPROVED",
            note="Row approved and locked"
        )

        return Response({"message": "Row approved and locked"})


class RejectRowView(APIView):
    def post(self, request, row_id):
        row = ActivityRow.objects.get(id=row_id)

        row.status = "REJECTED"
        row.rejected_at = timezone.now()
        row.save()

        AuditLog.objects.create(
            row=row,
            action="REJECTED",
            note="Row rejected"
        )

        return Response({"message": "Row rejected"})


class DeleteRowView(APIView):
    def delete(self, request, row_id):
        row = ActivityRow.objects.get(id=row_id)
        row.delete()

        return Response({"message": "Row deleted"})
import io
import calendar


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from datetime import datetime
from django.http import FileResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

from .models import DailyTrack
from .serializers import DailyTrackSerializer

# Create your views here.
class DailyTrackViewCRUDView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        daily_tracks = DailyTrack.objects.filter(user=request.user)
        serializer = DailyTrackSerializer(daily_tracks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DailyTrackSerializer(data=request.data)
        request.data['user'] = request.user.id
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        daily_track = DailyTrack.objects.get(user=user)
        serializer = DailyTrackSerializer(daily_track, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        user = request.user
        daily_track = DailyTrack.objects.get(user=user)
        serializer = DailyTrackSerializer(daily_track, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DownloadMonthlyReportAPIView(APIView):
    """
    APIView to generate and download a monthly PDF report for the authenticated user's DailyTrack data.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month):
        """
        Generate and return a PDF file containing DailyTrack records for the authenticated user.
        """
        # Convert month number to full name
        month_name = calendar.month_name[int(month)]
        user = request.user  # Get the logged-in user

        # Fetch records for the authenticated user
        daily_records = DailyTrack.objects.filter(user=user, date__year=year, date__month=month)

        if not daily_records.exists():
            return Response({"message": f"No records found for {month_name} {year}."}, status=404)

        # Create an in-memory buffer
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        pdf.setTitle(f"HealthTrack Report - {month_name} {year}")

        # Set title
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(150, 800, f"HealthTrack Report - {month_name} {year}")

        # Table headers
        data = [["Date", "Break Bleed", "Treatment", "Injection", "Physiotherapy"]]

        # Populate table with user data
        for record in daily_records:
            data.append([
                record.date.strftime("%d-%b-%Y"),
                record.break_through_bleed,
                record.treatment_for_bleed if record.treatment_for_bleed else "-",
                record.inj_hemilibra,
                record.physiotherapy
            ])

        # Create and style table
        table = Table(data, colWidths=[100, 100, 150, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Draw table
        table.wrapOn(pdf, 500, 700)
        table.drawOn(pdf, 50, 650 - (len(data) * 20))

        # Finalize PDF
        pdf.showPage()
        pdf.save()

        # Move buffer to start
        buffer.seek(0)

        # Return PDF response
        return FileResponse(buffer, as_attachment=True, filename=f"HealthTrack_{user.username}_{month_name}_{year}.pdf")
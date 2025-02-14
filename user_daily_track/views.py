import io
import calendar
from datetime import datetime

# these are rest_framework imports 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# these are django imports
from django.http import FileResponse

# these are reportlab imports
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# these are local imports
from .models import DailyTrack
from .serializers import DailyTrackSerializer
from user_profile.models import Profile
from user_profile.serializers import ProfileSerializer
from user.models import User

# Create your views here.
class DailyTrackViewCRUDView(APIView):

    """
    APIView to perform CRUD operations on DailyTrack data for the authenticated user.

    Allows the authenticated user to:
    - Get their DailyTrack data via a GET request.
    - Create new DailyTrack records via a POST request.
    - Update existing DailyTrack data via a PUT request.
    - Partially update existing DailyTrack data via a PATCH request.

    Permissions:
    - Requires the user to be authenticated.

    Methods:
    - GET: Fetch all DailyTrack records for the authenticated user.
    - POST: Create a new DailyTrack record for the authenticated user.
    - PUT: Fully update an existing DailyTrack record for the authenticated user.
    - PATCH: Partially update an existing DailyTrack record for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Fetch all DailyTrack records for the authenticated user.

        Returns:
        - 200 OK with the list of DailyTrack records if successful.
        - 404 NOT FOUND if no records are found for the user.
        """

        daily_tracks = DailyTrack.objects.filter(user=request.user)
        serializer = DailyTrackSerializer(daily_tracks, many=True)
        return Response(serializer.data)

    def post(self, request):

        """
        Create a new DailyTrack record for the authenticated user.

        Accepts:
        - POST request with DailyTrack data.

        Returns:
        - 201 CREATED with the new DailyTrack record data if successful.
        - 400 BAD REQUEST if the data is invalid.
        """
        serializer = DailyTrackSerializer(data=request.data)
        request.data['user'] = request.user.id
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):

        """
        Fully update an existing DailyTrack record for the authenticated user.

        Accepts:
        - PUT request with updated DailyTrack data.

        Returns:
        - 200 OK with the updated DailyTrack record data if successful.
        - 400 BAD REQUEST if the data is invalid.
        """
        user = request.user
        daily_track = DailyTrack.objects.get(user=user)
        serializer = DailyTrackSerializer(daily_track, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):

        """
        Partially update an existing DailyTrack record for the authenticated user.

        Accepts:
        - PATCH request with partial DailyTrack data.

        Returns:
        - 200 OK with the partially updated DailyTrack record data if successful.
        - 400 BAD REQUEST if the data is invalid.
        """
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
    This view generates a PDF report with the user's health data for a specified month and year.
    The PDF contains the user's personal details, medical profile, and daily health records for the month.

    Permissions:
    - Requires the user to be authenticated.

    Methods:
    - GET: Generate and download the monthly PDF report.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month):
        """
        Generate and return a PDF file containing DailyTrack records for the authenticated user.
         Accepts:
        - year: The year for the report (e.g., 2025).
        - month: The month for the report (1-12).

        Returns:
        - A PDF file containing the health report for the specified month and year.
        - 404 NOT FOUND if no records exist for the specified month and year.
        - 404 NOT FOUND if the user profile is not found.
        
        """
        month_name = calendar.month_name[int(month)]
        user = request.user  # Get logged-in user

        # Fetch the user's profile
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found."}, status=404)

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

        # Add user profile details
        pdf.setFont("Helvetica", 11)

        # Left column (Personal & Contact Details) - Left Aligned
        left_x = 50
        right_x = 550  # Right-aligned start position
        y_start = 770
        line_spacing = 15

        pdf.drawString(left_x, y_start, f"Name: {user.first_name} {user.last_name}")
        pdf.drawString(left_x, y_start - line_spacing, f"Email: {user.email}")
        pdf.drawString(left_x, y_start - 2 * line_spacing, f"Phone: {user.phone_number if user.phone_number else 'N/A'}")
        pdf.drawString(left_x, y_start - 3 * line_spacing, f"Date of Birth: {user.date_of_birth.strftime('%d-%b-%Y') if user.date_of_birth else 'N/A'}")

        # Format Address with City, State, Country
        address = f"{user.address if user.address else ''}, {user.city if user.city else ''}, {user.state if user.state else ''}, {user.country if user.country else 'N/A'}"
        address = address.replace(" ,", "").strip(", ")  # Remove empty values

        pdf.drawString(left_x, y_start - 4 * line_spacing, f"Address: {address}")
        pdf.drawString(left_x, y_start - 5 * line_spacing, f"Zip Code: {user.zip_code if user.zip_code else 'N/A'}")

        # Right column (Medical Details) - Right Aligned
        pdf.drawRightString(right_x, y_start, f"KA Regd No: {profile.ka_regd_no}")
        pdf.drawRightString(right_x, y_start - line_spacing, f"Hemophilia Type: {profile.heamophilia_type if profile.heamophilia_type else 'N/A'}")
        pdf.drawRightString(right_x, y_start - 2 * line_spacing, f"Factor: {profile.factor if profile.factor else 'N/A'}")
        pdf.drawRightString(right_x, y_start - 3 * line_spacing, f"Inhibitor: {profile.inhibitor if profile.inhibitor else 'N/A'}")
        pdf.drawRightString(right_x, y_start - 4 * line_spacing, f"Inhibitor %: {profile.inhibitor_percentage if profile.inhibitor_percentage else 'N/A'}")
        pdf.drawRightString(right_x, y_start - 5 * line_spacing, f"Target Joints: {profile.target_joints if profile.target_joints else 'N/A'}")

        # Adjust starting position for the table
        table_y_start = y_start - 12 * line_spacing

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
        table = Table(data, colWidths=[100, 100, 100, 100, 100])
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
        table.drawOn(pdf, 50, table_y_start)

        # Finalize PDF
        pdf.showPage()
        pdf.save()

        # Move buffer to start
        buffer.seek(0)

        # Return PDF response
        return FileResponse(buffer, as_attachment=True, filename=f"HealthTrack_{user.username}_{month_name}_{year}.pdf")

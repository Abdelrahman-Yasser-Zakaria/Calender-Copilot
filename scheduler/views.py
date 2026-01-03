from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .services.ai_service import parse_availability_with_gemini
from .utils.mongo import get_db_handle
from datetime import datetime
from bson import ObjectId

class GenerateScheduleView(APIView):
    def post(self, request):
        text = request.data.get('text')
        if not text:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)

        slots = parse_availability_with_gemini(text)
        
        if "error" in slots:
             return Response(slots, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"slots": slots}, status=status.HTTP_200_OK)

class SaveScheduleView(APIView):
    def post(self, request):
        tutor_name = request.data.get('tutor_name')
        raw_input = request.data.get('raw_input')
        slots = request.data.get('slots')

        if not tutor_name or not slots:
            return Response({"error": "Missing tutor_name or slots"}, status=status.HTTP_400_BAD_REQUEST)

        db, _ = get_db_handle()
        collection = db['tutor_profiles']

        document = {
            "tutor_name": tutor_name,
            "created_at": datetime.now().isoformat(),
            "raw_input": raw_input,
            "availability_slots": slots
        }

        result = collection.insert_one(document)
        
        return Response({
            "status": "success",
            "tutor_id": str(result.inserted_id)
        }, status=status.HTTP_201_CREATED)

def index(request):
    return render(request, 'index.html')
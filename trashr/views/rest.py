from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from trashr.serializers import ReadingSerializer


class CreateReading(APIView):

    def post(self, request, format=None):
        # Make the string that was sent into a dictionary
        serializer = ReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

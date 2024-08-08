from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from os import listdir
from os.path import isfile, join
from PIL import Image

import face_recognition
import re
import requests

from .serializers import OnlineAttendanceSerializer

encodings = []
encoding_name = []


class OnlineAttendanceView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = OnlineAttendanceSerializer(data=request.data)
        if (serializer.is_valid()):
            imageUrls = serializer.validated_data['imageUrls']
            for imageUrl in imageUrls:
                self.downloadImage(url=imageUrl)
            present_student = self.scan()
            print("present_student",present_student)
            return Response(present_student, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def getEncodings(self):
        image_directory = 'D:\me\\backend\\django_projects\\attendance_log\\attendance\\static\\attendance\\images'
        image_files = [f for f in listdir(image_directory) if (
            isfile(join(image_directory, f)))]
        # print(image_files)
        for image_file in image_files:
            img = Image.open(f'{image_directory}/{image_file}')
            matches = re.split("^[0-9]_(.*) - (.*)(\..*)", image_file)
            image_name = matches[1]
            image = face_recognition.load_image_file(
                f'{image_directory}/{image_file}')
            image_encoding = face_recognition.face_encodings(
                image, known_face_locations=[(0, img.width, img.height, 0)])[0]
            # print('image_encoding', image_encoding)
            encodings.append(image_encoding)
            encoding_name.append(image_name)

    def downloadImage(self, url):
        print("downloading image")
        image_download_directory = 'D:\me\\backend\\django_projects\\attendance_log\\attendance\\static\\attendance\\images\\download'
        with open(f'{image_download_directory}\image.jpg', 'wb') as handle:
            response = requests.get(url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

    def scan(self):
        identified_student = set()
        if (not encodings):
            print("generating Encodings")
            self.getEncodings()
            print("generating Encodings successfull")
            # print('encodings', encodings)
        attendance_image_directory = 'D:\me\\backend\\django_projects\\attendance_log\\attendance\\static\\attendance\\images\\download'
        attendance_image_files = [f for f in listdir(attendance_image_directory) if (
            isfile(join(attendance_image_directory, f)))]
        for image_file in attendance_image_files:
            print(f"Identifying Students in {image_file}")
            img = Image.open(f'{attendance_image_directory}/{image_file}')
            image = face_recognition.load_image_file(
                f'{attendance_image_directory}/{image_file}')
            attendance_image_encoding = face_recognition.face_encodings(
                image, known_face_locations=[(0, img.width, img.height, 0)])[0]
            results = face_recognition.compare_faces(
                encodings, attendance_image_encoding)
            for i in range(0, len(encoding_name)):
                if results[i]:
                    identified_student.add(encoding_name[i])
        present = [student for student in identified_student]
        result = {
            'students': present
        }
        return result

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from os import listdir, remove
from os.path import isfile, join, splitext
from PIL import Image
from pillow_heif import register_heif_opener

import re
import requests
import numpy as np
from imutils import paths
import face_recognition
from deepface import DeepFace
from scipy.spatial import distance
from pathlib import Path
import pickle
import cv2
import os
import json
import shutil
from .constants import allStudents
from .serializers import OnlineAttendanceSerializer

encodings = []
encoding_name = []
attendance_image_directory = 'D:\me\\backend\\django_projects\\attendance_log\\attendance\\static\\attendance\\images\\download\\'
student_image_directory = 'D:\me\\backend\\django_projects\\attendance_log\\attendance\\static\\attendance\\images\\student\\'
image_download_directory = 'D:\me\\backend\\django_projects\\attendance_log\\attendance\\static\\attendance\\images\\download'
cascPathface = 'D:\me\\backend\django_projects\\attendance_log\\attendance\static\\attendance\haarcascade_frontalface_alt2.xml'


class OnlineAttendanceView(APIView):
    authentication_classes = []
    permission_classes = []
    db_embeddings = {}

    def post(self, request, *args, **kwargs):
        serializer = OnlineAttendanceSerializer(data=request.data)
        if (serializer.is_valid()):
            # self.getEncodings()
            # return Response({"message": "Encodings generated successfully"}, status=status.HTTP_200_OK)
            imageUrls = serializer.validated_data['imageUrls']
            # for (i, imageUrl) in enumerate(imageUrls):
            #     self.downloadImage(url=imageUrl, image_name=i)
            model_backend_detectors = [
                # {"model_name": "Dlib", "face_extractor_detector_backend": "dlib",
                #     "db_detector_backend": "dlib", "distance_metric": "cosine"},
                # {"model_name": "VGG-Face", "face_extractor_detector_backend": "centerface",
                #  "db_detector_backend": "centerface", "distance_metric": "cosine"},
                {"model_name": "VGG-Face", "face_extractor_detector_backend": "yolov8",
                    "db_detector_backend": "yolov8", "distance_metric": "cosine"},
                # {"model_name": "Facenet", "face_extractor_detector_backend": "yunet",
                #     "db_detector_backend": "yunet", "distance_metric": "cosine"},
                # {"model_name": "VGG-Face", "face_extractor_detector_backend": "fastmtcnn", "db_detector_backend": "fastmtcnn", "distance_metric": "cosine"},
                # {"model_name": "VGG-Face", "face_extractor_detector_backend": "retinaface",
                #     "db_detector_backend": "retinaface", "distance_metric": "cosine"},
                # {"model_name": "VGG-Face", "face_extractor_detector_backend": "retinaface",
                #     "db_detector_backend": "yunet", "distance_metric": "cosine"},
            ]
            present_student = set()
            for model_backend_detector in model_backend_detectors:
                student = self.deepFaceScan(
                    model_name=model_backend_detector["model_name"],
                    face_extractor_detector_backend=model_backend_detector[
                        "face_extractor_detector_backend"],
                    db_detector_backend=model_backend_detector["db_detector_backend"],
                    distance_metric=model_backend_detector["distance_metric"])
                present_student = present_student.union(student)
            # present_student = self.scan()
            present_student = list(present_student)
            present_student.sort()
            print("present_student", present_student)
            result = {
                'students': present_student
            }
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def getEncodings(self):
        imagePaths = list(paths.list_images(student_image_directory))
        knownEncodings = []
        knownNames = []
        for (i, imagePath) in enumerate(imagePaths):
            name = imagePath.split(os.path.sep)[-1]
            print(f'generating encoding for: {name}')
            matches = re.split("^[0-9]_(.*) - (.*)(\..*)", name)
            student_name = matches[1]
            # load the input image and convert it from BGR (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Use Face_recognition to locate faces
            boxes = face_recognition.face_locations(rgb, model='hog')
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            # loop over the encodings
            # print(f"Encoding size for {name} {len(encodings)}")
            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(student_name)
            # save encodings along with their names in dictionary data
        data = {"encodings": knownEncodings, "names": knownNames}
        # use pickle to save data into a file for later use
        f = open("attendance\\static\\attendance\\face_enc", "wb")
        f.write(pickle.dumps(data))
        f.close()

    def downloadImage(self, url, image_name):
        print("downloading image")
        with open(f'{image_download_directory}\{image_name}.jpg', 'wb') as handle:
            response = requests.get(url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

    def scan(self):
        # load the harcaascade in the cascade classifier
        faceCascade = cv2.CascadeClassifier(cascPathface)
        total_student_face = 0
        # load the known faces and embeddings saved in last file
        data = pickle.loads(
            open('attendance\\static\\attendance\\face_enc', "rb").read())
        # Find path to the image you want to detect face and pass it here
        attendance_image_files = [f for f in listdir(attendance_image_directory) if (
            isfile(join(attendance_image_directory, f)))]
        identified_student = set()
        for image_file in attendance_image_files:
            print(f"Identifying Students in {image_file}")
            image = cv2.imread(
                f'{attendance_image_directory}\\{image_file}')
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # the facial embeddings for face in input
            encodings = face_recognition.face_encodings(rgb)
            print(f"Total faces found in {image_file} {len(encodings)}")
            total_student_face += len(encodings)
            # loop over the facial embeddings incase we have multiple embeddings for multiple fcaes
            for encoding in encodings:
                # Compare encodings with encodings in data["encodings"]
                # Matches contain array with boolean values and True for the embeddings it matches closely
                # and False for rest
                matches = face_recognition.compare_faces(data["encodings"],
                                                         encoding, tolerance=0.5)
                # set name =inknown if no encoding matches
                name = "Unknown"
                # check to see if we have found a match
                if True in matches:
                    # Find positions at which we get True and store them
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        # Check the names at respective indexes we stored in matchedIdxs
                        name = data["names"][i]
                        # increase count for the name we got
                        counts[name] = counts.get(name, 0) + 1
                        # set name which has highest count
                        name = max(counts, key=counts.get)

                    # update the list of names
                    identified_student.add(name)
        present = [student for student in identified_student]
        print(f"total students identified in images {total_student_face}")
        print(f"total students matched in images {len(present)}")
        result = {
            'students': present
        }
        print("deleting downloaded images...")
        image_download_directory = 'D:\me\\backend\\django_projects\\attendance_log\\attendance\\static\\attendance\\images\\download\\'
        imagePaths = list(paths.list_images(image_download_directory))
        for imagePath in imagePaths:
            name = imagePath.split(os.path.sep)[-1]
            print(f"deleting {name}")
            try:
                if os.path.isfile(imagePath) or os.path.islink(imagePath):
                    os.unlink(imagePath)
                elif os.path.isdir(imagePath):
                    shutil.rmtree(imagePath)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (imagePath, e))
        return result

    def save_embeddings(self, model_name, detector_backend):
        print(f"Creating embedding for {model_name}, {detector_backend}")
        embeddings = {}

        for root, dirs, files in os.walk(student_image_directory):
            for file in files:
                if file.endswith(("jpg", "jpeg", "png")):
                    img_path = os.path.join(root, file)
                    print(
                        f"Creating embedding for {os.path.splitext(file)[0]}")
                    embedding = DeepFace.represent(
                        img_path=img_path,
                        model_name=model_name,
                        detector_backend=detector_backend,
                        enforce_detection=False
                    )

                    embeddings[file] = embedding[0]["embedding"]

        with open(f"attendance\\static\\attendance\\face_embeddings_{model_name}_{detector_backend}.json", "w") as f:
            json.dump(embeddings, f)

    def load_embeddings(self, model_name, detector_backend):
        filepath = Path(
            f"attendance\\static\\attendance\\face_embeddings_{model_name}_{detector_backend}.json")
        if not filepath.exists():
            self.save_embeddings(model_name=model_name,
                                 detector_backend=detector_backend)
        with open(filepath, "r") as f:
            self.db_embeddings = json.load(f)

    def extract_faces_retina(self, image_path, detector_backend):
        face_dicts = DeepFace.extract_faces(
            img_path=image_path, detector_backend=detector_backend, enforce_detection=False, align=True)
        faces = []
        for face_dict in face_dicts:
            faces.append(face_dict['face'])
        return faces

    # Find the best match for a single face embedding
    def find_best_match(self, face_embedding, distance_metric="cosine", threshold=0.6):
        best_match = None
        best_distance = float("inf")
        # Iterate over each precomputed embedding
        for img_name, embedding in self.db_embeddings.items():
            # Calculate the distance between face_embedding and precomputed embedding
            if distance_metric == "cosine":
                dist = distance.cosine(face_embedding, embedding)
            elif distance_metric == "euclidean":
                dist = distance.euclidean(face_embedding, embedding)
            else:  # Euclidean L2
                dist = distance.euclidean(face_embedding, embedding) ** 2

            # Check if it's the best match within the threshold
            if dist < best_distance and dist < threshold:
                best_match = img_name
                best_distance = dist

        return best_match, best_distance

    # Step 2: Recognize each face in the image
    def recognize_faces_in_image(self, model_name, face_extractor_detector_backend, db_detector_backend, distance_metric):
        # Extract faces from the image
        self.load_embeddings(
            model_name=model_name, detector_backend=face_extractor_detector_backend)
        data = Path(
            f'attendance\\static\\attendance\\face_enc_{face_extractor_detector_backend}')
        extracted_face = []
        if data.exists():
            extracted_face = pickle.loads(
                open(f'attendance\\static\\attendance\\face_enc_{face_extractor_detector_backend}', "rb").read())
        identified_student = set()
        imagePaths = list(paths.list_images(attendance_image_directory))
        if not extracted_face:
            print("Generating extracted faces")
            for imagePath in imagePaths:
                name = imagePath.split(os.path.sep)[-1]
                print(f"Extracting faces from: {name}")
                extracted_face += self.extract_faces_retina(
                    image_path=imagePath, detector_backend=face_extractor_detector_backend)
                f = open(
                    f"attendance\static\\attendance\\face_enc_{face_extractor_detector_backend}", "wb")
                f.write(pickle.dumps(extracted_face))
        print(f"total extracted faces: {len(extracted_face)}")

        for i, face in enumerate(extracted_face):
            # Step 3: Generate the embedding for the face
            face_embedding = DeepFace.represent(
                img_path=face,  # passing the cropped face
                model_name=model_name,
                detector_backend=face_extractor_detector_backend,
                enforce_detection=False
            )[0]["embedding"]

            # Step 4: Find the best match for this face
            print("Checking match for face: ", i)
            best_match, best_distance = self.find_best_match(
                face_embedding, self.db_embeddings)
            if best_match:
                file_name = best_match.split(os.path.sep)[-1]
                student_name = re.split(
                    "^[0-9]_(.*) - (.*)(\..*)", file_name)[1]
                identified_student.add(student_name)
        notPresent = []
        for student in allStudents:
            if student not in identified_student:
                notPresent.append(student)
        print(f"total students matched in images {len(identified_student)}")
        print(f"total students not matched in images {len(notPresent)}")
        print(f"Not Present: {notPresent}")
        return identified_student

    def deepFaceScan(self, model_name, face_extractor_detector_backend, db_detector_backend, distance_metric):
        print(
            f"Executing deepface scan with {model_name} model, {face_extractor_detector_backend} for face extraction,{db_detector_backend} as db detector backed and {distance_metric} distance metric")
        # return self.recognize_faces_in_image(
        #     model_name=model_name,
        #     face_extractor_detector_backend=face_extractor_detector_backend,
        #     db_detector_backend=db_detector_backend,
        #     distance_metric=distance_metric)
        data = Path(
            f'attendance\\static\\attendance\\face_enc_{face_extractor_detector_backend}')
        extracted_face = []
        if data.exists():
            extracted_face = pickle.loads(
                open(f'attendance\\static\\attendance\\face_enc_{face_extractor_detector_backend}', "rb").read())
        identified_student = set()
        imagePaths = list(paths.list_images(attendance_image_directory))
        if not extracted_face:
            print("Generating extracted faces")
            for imagePath in imagePaths:
                name = imagePath.split(os.path.sep)[-1]
                print(f"Extracting faces from: {name}")
                extracted_face += self.extract_faces_retina(
                    image_path=imagePath, detector_backend=face_extractor_detector_backend)
                f = open(
                    f"attendance\static\\attendance\\face_enc_{face_extractor_detector_backend}", "wb")
                f.write(pickle.dumps(extracted_face))
        print(f"total extracted faces: {len(extracted_face)}")
        for face_index, face in enumerate(extracted_face):
            matches = []
            print(f'Matching face: {face_index}')
            dfs = DeepFace.find(
                face, db_path=student_image_directory, model_name=model_name, detector_backend=db_detector_backend,
                # distance_metric=distance_metric,
                enforce_detection=False, silent=True, align=True)
            for df in dfs:
                if not df.empty:
                    for _, match in df.iterrows():
                        matches.append((match['identity'], match['distance']))
            matches.sort(key=lambda x: x[1])
            if matches:
                best_matches = matches[:1]
                for identity, distance in best_matches:
                    if distance > 0.6:
                        continue
                    file_name = identity.split(os.path.sep)[-1]
                    student_name = re.split(
                        "^[0-9]_(.*) - (.*)(\..*)", file_name)[1]
                    identified_student.add(student_name)
            else:
                pass
        notPresent = []
        for student in allStudents:
            if student not in identified_student:
                notPresent.append(student)
        print(f"total students matched in images {len(identified_student)}")
        print(f"total students not matched in images {len(notPresent)}")
        print(f"Not Present: {notPresent}")
        return identified_student

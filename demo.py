 # from fastapi import FastAPI, File, UploadFile, status
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# import face_recognition
# from typing import List


# app = FastAPI()


# class Result(BaseModel):
#     match: bool
#     # error: str = None
#     responseMessage: str = None


# @app.post("/images", response_model=Result, status_code=status.HTTP_200_OK)
# async def post_images(file1: UploadFile = File(...), file2: UploadFile = File(None)):
#     if file1 is None:
#         return Result(match=False, responseMessage="file1 parameter Required")
#     if file2 is None:
#         return Result(match=False, responseMessage="file2 parameter Required")

#     if not file1.filename:
#         return Result(match=False, responseMessage="file1 is empty or not provided")
#     if not file2.filename:
#         return Result(match=False, responseMessage="file2 is empty or not provided")

#     # Validate file extensions (you can add more allowed extensions if needed)
#     allowed_extensions = {"jpg", "jpeg", "png", "gif"}
#     file1_extension = file1.filename.split(".")[-1].lower()
#     file2_extension = file2.filename.split(".")[-1].lower()

#     if file1_extension not in allowed_extensions:
#         return Result(match=False, responseMessage="Invalid file format for file1")
#     if file2_extension not in allowed_extensions:
#         return Result(match=False, responseMessage="Invalid file format for file2")

#     try:
#         first_image = face_recognition.load_image_file(file1.file)
#         second_image = face_recognition.load_image_file(file2.file)

#         first_face_encodings = face_recognition.face_encodings(first_image)
#         second_face_encodings = face_recognition.face_encodings(second_image)

#         first_face_detected = len(first_face_encodings) > 0
#         second_face_detected = len(second_face_encodings) > 0

#         if not first_face_detected and not second_face_detected:
#             return Result(
#                 match=False, responseMessage="No face detected in both images"
#             )
#         elif not first_face_detected:
#             return Result(match=False, responseMessage="No face detected in file1")
#         elif not second_face_detected:
#             return Result(match=False, responseMessage="No face detected in file2")
#         else:
#             first_face_encoding = first_face_encodings[0]
#             second_face_encoding = second_face_encodings[0]

#             result = face_recognition.compare_faces(
#                 [first_face_encoding], second_face_encoding
#             )

#             # return Result(match=result[0])
#             return Result(match=result[0], responseMessage="Face match successfully")

#     except FileNotFoundError:
#         return Result(match=False, responseMessage="File not found")

#     except Exception as e:
#         return Result(match=False, responseMessage=f"Error: {str(e)}")
from fastapi import FastAPI, File, UploadFile, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import face_recognition

app = FastAPI()

class Result(BaseModel):
    match: bool
    responseMessage: str = None
    responseCode: int

@app.post("/images", response_model=Result)
async def post_images(file1: UploadFile = File(None), file2: UploadFile = File(None)):
    if file1 is None:
        return Result(match=False, responseCode=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, responseMessage="File1 parameter Required")

    if file2 is None:
        return Result(match=False, responseCode=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, responseMessage="File2 parameter Required")

    if not file1.filename:
        return Result(match=False, responseCode=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, responseMessage="File1 is empty or not Provided.")
    if not file2.filename:
        return Result(match=False, responseCode=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, responseMessage="File2 is empty or not Provided.")

    # Validate file extensions (you can add more allowed extensions if needed)
    allowed_extensions = {"jpg", "jpeg", "png"}
    file1_extension = file1.filename.split(".")[-1].lower()
    file2_extension = file2.filename.split(".")[-1].lower()

    if file1_extension not in allowed_extensions:
        return Result(match=False, responseCode=status.HTTP_400_BAD_REQUEST, responseMessage="Invalid File format for file1")
    if file2_extension not in allowed_extensions:
        return Result(match=False, responseCode=status.HTTP_400_BAD_REQUEST, responseMessage="Invalid File format for file2")

    try:
        first_image = face_recognition.load_image_file(file1.file)
        second_image = face_recognition.load_image_file(file2.file)

        first_face_encodings = face_recognition.face_encodings(first_image)
        second_face_encodings = face_recognition.face_encodings(second_image)

        first_face_detected = len(first_face_encodings) > 0
        second_face_detected = len(second_face_encodings) > 0

        if not first_face_detected and not second_face_detected:
            return Result(match=False, responseCode=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, responseMessage="No face detected in both images.")
        elif not first_face_detected:
            return Result(match=False, responseCode=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, responseMessage="No face detected in first Image.")
        elif not second_face_detected:
            return Result(match=False, responseCode=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, responseMessage="No face detected in second Image.")
        else:
            first_face_encoding = first_face_encodings[0]
            second_face_encoding = second_face_encodings[0]

            result = face_recognition.compare_faces(
                [first_face_encoding], second_face_encoding
            )

            if result[0] == True:
                return Result(match=True, responseMessage="Face match successfully", responseCode=status.HTTP_200_OK)
            else:
                return Result(match=False, responseMessage="No face match found", responseCode=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    except FileNotFoundError:
        return Result(match=False, responseCode=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, responseMessage="File not found.")

    except Exception as e:
        return Result(match=False, responseCode=status.HTTP_400_BAD_REQUEST, responseMessage=f"Error: {str(e)}")

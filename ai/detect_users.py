import boto3

BUCKET_ID = "choggers-faces"
COLLECTION_ID = "choggers-faces"

def get_face_data(path, name):
    s3client = boto3.client("s3")
    rkclient = boto3.client("rekognition")

    s3client.upload_file(path, BUCKET_ID, name)

    response = rkclient.index_faces(
        CollectionId=COLLECTION_ID,
        Image={
            "S3Object": {
                "Bucket": BUCKET_ID,
                "Name": name,
            },
        },
    )

    faces = response["FaceRecords"]
    face_data = []
    names = []

    for face in faces:
        faceid = face["Face"]["FaceId"]
        
        face_data.append({
            "faceid": faceid,
            "box": face["Face"]["BoundingBox"],
        })

        search_response = rkclient.search_users(
            CollectionId=COLLECTION_ID,
            FaceId=faceid,
            UserMatchThreshold=50,
        )

        matches = sorted(
            search_response["UserMatches"],
            key=lambda match: match["Similarity"],
            reverse=True,
        )

        face_data[-1]["userid"] = \
            matches[0]["User"]["UserId"] if len(matches) else None
        names.append(face_data[-1]["userid"])
    print(face_data)

    # Cleanup
    if len(face_data):
        rkclient.delete_faces(
            CollectionId=COLLECTION_ID,
            FaceIds=[face["faceid"] for face in face_data],
        )

    s3client.delete_object(Bucket=BUCKET_ID, Key=name)

    return face_data, names


import boto3

BUCKET_ID = "choggers-faces"
COLLECTION_ID = "choggers-faces"

def main():
    s3client = boto3.client("s3")
    rkclient = boto3.client("rekognition")

    # Cleanup
    rkclient.delete_collection(CollectionId=COLLECTION_ID)
    rkclient.create_collection(CollectionId=COLLECTION_ID)

    images = s3client.list_objects_v2(Bucket=BUCKET_ID)
    processed_users = {}

    for image in images["Contents"]:
        fid = image["Key"]
        uid = fid.split("/")[0]
        print(f"Processing {fid}.")

        if uid not in processed_users:
            print(f"New user {uid} detected.")
            processed_users[uid] = True
            rkclient.create_user(CollectionId=COLLECTION_ID, UserId=uid)
            
        response = rkclient.index_faces(
            CollectionId=COLLECTION_ID,
            Image={
                "S3Object": {
                    "Bucket": BUCKET_ID,
                    "Name": fid,
                },
            },
            MaxFaces=1,
        )

        print(f"Indexed {fid}.")
        faces = response["FaceRecords"]

        if len(faces) != 1:
            print(f"Error: {len(faces)} faces detected in {fid}.")
        else:
            faceid = faces[0]["Face"]["FaceId"]
            
            rkclient.associate_faces(
                CollectionId=COLLECTION_ID,
                UserId=uid,
                FaceIds=[faceid],
            )

            print(f"Completed processing {fid}.")

if __name__ == "__main__":
    main()

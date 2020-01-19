import boto3

s3 = boto3.client('s3')

def list_videos(bucket):
    videos = []

    for key in s3.list_objects(Bucket=bucket)['Contents']:
        if ".mp4" in key['Key']:
            videos.append(key['Key'])

    videos.sort()

    return ", ".join(videos)

def update_video_index(bucket, videos):
    index_file = 'index.txt'

    s3.put_object(
        Body=videos,
        Bucket=bucket,
        Key=index_file,
        ACL='public-read'
    )

def upload_video(path, bucket, name):
    with open(path, "rb") as file:
        s3.upload_fileobj(
            file,
            bucket,
            name,
            ExtraArgs={'ACL':'public-read'}
        )

    # after the video is uploaded we update the index
    videos = list_videos(bucket)
    update_video_index(bucket, videos)

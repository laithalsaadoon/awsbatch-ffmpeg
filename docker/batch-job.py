import boto3
import ffmpeg
import subprocess
import sys

subprocess.call('sudo mount -t nfs -o nolock <CHANGE ME: File Gateway Endpoint> /mnt/fgw', shell=True)

s3 = boto3.client('s3')
bucket = sys.argv[1]

videos = ['forest.mp4']
presigned_urls = []

for video in videos:
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': video
        }
    )
    presigned_urls.append(url)

ffmpeg.input(presigned_urls[0]).output('/mnt/fgw/forest_%04d.png').run()
# AWS Batch for Video to Frames Processing

Pre-requisites:
Local machine must have the AWS CLI configured with sufficient permissions to ECS Container Repository (ECR)
Docker command line tools
Working knowledge of Docker, Python, FFMPEG


## Storage in AWS

1. Create two buckets - one for raw videos, one for frames
2. Create a File Gateway on EC2: https://aws.amazon.com/premiumsupport/knowledge-center/file-gateway-ec2/
3. Point the File Gateway to the S3 bucket for frames
4. Upload a video to the video bucket

## Build Docker Image and Upload to ECR

In this step, we are building a docker image from scratch. We build an image based on Amazon Linux, and build FFMPEG from code. We also install tools to use AWS APIs from Python (boto3)

1. Install docker command line tools on your local machine
2. Create an ECR Repository in the AWS Console
3. Update the batch-job.py in this git repo with your File Gateway mount information where it says CHANGEME. Also update with the name of your video files.
4. From command line, change directories to /docker in this repo
5. ```docker build -t ffmpeg-amazonlinux .```
6. ```docker tag ffmpeg-amazonlinux:latest 392583147479.dkr.ecr.us-east-1.amazonaws.com/ffmpeg-amazonlinux:latest```
7. ```aws ecr get-login --no-include-email --region us-east-1```
8. Copy and paste the output of the above command
9. ```docker push <your ECR URL>/ffmpeg-amazonlinux:latest```

## AWS Batch

1. Configure AWS Batch in the AWS Console: https://docs.aws.amazon.com/batch/latest/userguide/Batch_GetStarted.html
2. Ensure the Compute Environment is configured with connectivity to the File Gateway. See AWS VPC and Security Groups for more details.
3. Create a job definition with your container image above
4. The command should be similar to ```python3 /batch/batch-job.py <your s3 bucket>```
5. Set the job definition to priviledged and user to root: https://docs.aws.amazon.com/batch/latest/userguide/create-job-definition.html
6. Submit the job to the job queue you created

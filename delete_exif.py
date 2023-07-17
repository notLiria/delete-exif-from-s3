import os
import boto3
from PIL import Image
from io import BytesIO


# AWS Credentials
aws_access_key_id = ''
aws_secret_access_key = ''
bucket_name = ''

# Connect to the AWS S3 bucket
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Get the list of all files in the bucket
response = s3.list_objects(Bucket=bucket_name)


for file in response['Contents']:
    # Only process files that are images
    if file['Key'].lower().endswith(('jpg', 'jpeg', 'png')):
        print(f"Processing file: {file['Key']}")

        # Get the file from S3
        img_object = s3.get_object(Bucket=bucket_name, Key=file['Key'])
        img_content = img_object['Body'].read()

        # Load the image with Pillow
        img = Image.open(BytesIO(img_content))

        # Remove EXIF data
        data = list(img.getdata())
        image_without_exif = Image.new(img.mode, img.size)
        image_without_exif.putdata(data)

        # Save the image to a BytesIO object in the same format as the original image
        byte_io = BytesIO()
        image_without_exif.save(byte_io, format=img.format)

        # Seek back to the start of the BytesIO object
        byte_io.seek(0)

        # Overwrite the original image on S3 in the same format as the original image
        content_type = 'image/jpeg' if img.format == 'JPEG' else 'image/png'
        s3.put_object(Body=byte_io, Bucket=bucket_name, Key=file['Key'], ContentType=content_type)

        print(f"Finished processing file: {file['Key']}")



print('Done!')

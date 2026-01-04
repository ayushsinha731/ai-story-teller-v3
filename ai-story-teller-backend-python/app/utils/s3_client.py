"""AWS S3 client for audio file storage."""
import boto3
from typing import Optional
from botocore.exceptions import ClientError
from app.config import settings
from app.utils.logger import logger


class S3Client:
    """S3 client for file operations."""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        self.bucket_name = settings.s3_bucket_name
    
    async def upload_audio(
        self,
        file_content: bytes,
        file_name: str,
        folder: str = "audio"
    ) -> tuple[str, str]:
        """
        Upload audio file to S3.
        
        Returns:
            tuple: (s3_key, s3_url)
        """
        try:
            # Generate S3 key (path)
            s3_key = f"{folder}/{file_name}"
            
            # Upload file
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType="audio/wav"
            )
            
            # Generate URL
            s3_url = f"https://{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{s3_key}"
            
            logger.info(f"Audio uploaded to S3: {s3_key}")
            return s3_key, s3_url
            
        except ClientError as e:
            logger.error(f"S3 upload error: {e}")
            raise Exception(f"Failed to upload file to S3: {str(e)}")

    async def upload_image(
        self,
        file_content: bytes,
        file_name: str,
        folder: str = "images"
    ) -> str:
        """
        Upload image bytes to S3.
        
        Returns:
            str: s3_url
        """
        try:
            # Generate S3 key
            s3_key = f"{folder}/{file_name}"
            
            # Upload file
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType="image/png"
            )
            
            # Generate URL
            s3_url = f"https://{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{s3_key}"
            
            logger.info(f"Image uploaded to S3: {s3_key}")
            return s3_url
            
        except ClientError as e:
            logger.error(f"S3 image upload error: {e}")
            raise Exception(f"Failed to upload image to S3: {str(e)}")
    
    def get_presigned_url(self, s3_key: str, expiration: int = 3600) -> str:
        """Generate presigned URL for temporary access."""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"S3 presigned URL error: {e}")
            raise Exception(f"Failed to generate presigned URL: {str(e)}")
    
    async def delete_audio(self, s3_key: str) -> None:
        """Delete audio file from S3."""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            logger.info(f"Audio deleted from S3: {s3_key}")
        except ClientError as e:
            logger.error(f"S3 delete error: {e}")
            raise Exception(f"Failed to delete file from S3: {str(e)}")


# Singleton instance
s3_client = S3Client()


import boto3

class S3Uploader:
    def __init__(self, bucket_name, aws_access_key, aws_secret_key, region_name):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )
        self.bucket_name = bucket_name

    def upload_file(self, file_stream, file_name):
        # Subir el archivo al bucket S3
        self.s3.upload_fileobj(
            file_stream,
            self.bucket_name,
            file_name,
            ExtraArgs={'ContentType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
        )

        # Obtener la URL del archivo
        file_url = f"https://{self.bucket_name}.s3.{self.s3.meta.region_name}.amazonaws.com/{file_name}"
        return file_url
import requests
from boto3 import client
from django.conf import settings
from django.http import JsonResponse
from urllib import parse
from civictechprojects.models import FileCategory

from pprint import pprint

class S3Key:
    def __init__(self, raw_key):
        key_parts = raw_key.split('/')
        self.file_category = key_parts[0]
        self.username = key_parts[1]
        self.file_name = key_parts[2]


def s3_key_to_public_url(key):
    return 'https://%s.s3.amazonaws.com/%s' % (settings.S3_BUCKET, parse.quote_plus(key))


def presign_s3_upload(raw_key, file_name, file_type, acl):
    s3 = client('s3')

    content_disposition = 'attachment; filename="{0}"'.format(file_name)
    presigned_post = s3.generate_presigned_post(
        Bucket=settings.S3_BUCKET,
        Key=raw_key,
        Fields={"acl": acl, "Content-Type": file_type, "Content-Disposition": content_disposition},
        Conditions=[
            {"acl": acl},
            {"Content-Type": file_type},
            {"Content-Disposition": content_disposition}
        ],
        ExpiresIn=3600
    )

    response = JsonResponse({
        'data': presigned_post,
        'url': s3_key_to_public_url(raw_key)
    })
    return response


def delete_s3_file(raw_key):
    s3 = client('s3')
    response = s3.delete_object(Bucket=settings.S3_BUCKET, Key=raw_key)
    return response


def user_has_permission_for_s3_file(username, raw_key):
    s3_key = S3Key(raw_key)
    return username == s3_key.username

# ACL, Body, Bucket, CacheControl, ContentDisposition, ContentEncoding, ContentLanguage, ContentLength, ContentMD5, ContentType, Expires, GrantFullControl, GrantRead, GrantReadACP, GrantWriteACP, Key,
# Metadata, ServerSideEncryption, StorageClass, WebsiteRedirectLocation, SSECustomerAlgorithm, SSECustomerKey, SSECustomerKeyMD5, SSEKMSKeyId, RequestPayer, Tagging

def copy_external_file_to_s3(file_url, source, owner):
    # Download external file
    print('Downloading ' + file_url)
    # TODO: Pick out more sensible key
    key = f'{source}/{owner.username}'
    print(key)
    file_name_parts = key.split('.')
    file_name = "".join(file_name_parts[:-1])
    # file_type = file_name_parts[-1]
    file_stream = requests.get(file_url, stream=True)
    pprint(file_stream)
    pprint(file_stream.headers)
    file_data = file_stream.raw.read()
    # TODO: Extract file type from stream header ('Content-Type': 'image/jpeg')
    content_type = file_stream.headers['Content-Type']
    print('Downloaded {url}, file size: {size}'.format(url=file_url, size=len(file_data)))
    s3 = client('s3')
    content_disposition = 'attachment; filename="{0}"'.format(file_name)
    response = s3.put_object(Body=file_data,
                             Bucket=settings.S3_BUCKET,
                             Key=key,
                             ACL='public-read',
                             ContentType=content_type,
                             ContentDisposition=content_disposition)
    pprint(response)

    return {
        'publicUrl': s3_key_to_public_url(key),
        'file_user': owner,
        'file_category': FileCategory.THUMBNAIL.value,
        'visibility': 'PUBLIC',
        'fileName': f'{owner.first_name}{owner.last_name}_thumbnail.{source} avatar',
        'key': key
    }


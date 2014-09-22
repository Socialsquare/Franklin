"""
Django settings for global_change_lab project in production.

!! THIS FILE IS CONFIDENTIAL !!

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from global_change_lab.settings import *

import sys
sys.path.append(BASEDIR) # As this holds the S3 module.

from storages.utils.S3 import CallingFormat
AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

### Configure S3
# These are the keys for your created IAM user
AWS_ACCESS_KEY_ID = '<YOUR ACCESS KEY ID>'
AWS_SECRET_ACCESS_KEY = '<YOUR SECRET ACCESS KEY>'
AWS_STORAGE_BUCKET_NAME = '<YOUR BUCKET NAME>'

### Media files (uploads): use Amazon S3
DEFAULT_FILE_STORAGE = 'global_change_lab.s3utils.MEDIA_PREPENDED_S3_STORAGE'
MEDIA_URL = 'http://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME

### Staticfiles: use Amazon S3
STATICFILES_STORAGE = 'global_change_lab.s3utils.STATIC_PREPENDED_S3_STORAGE'
S3_URL = 'http://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL
AWS_PRELOAD_METADATA = True # Only upload new files (doesn't actually work)
                            # we use "github.com/antonagestam/collectfast"
                            # in order to only upload new/updated files

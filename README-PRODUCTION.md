Franklin in production
======================

Amazon S3
---------
Franklin uses Amazon S3 as backend image host to save bandwidth costs and in
some cases because cloud providers (like Heroku and cloudControl) don't provide
static file hosting.

S3 is used for static files in django and media uploaded to your Franklin
instance.

Insert your AWS credentials

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_STORAGE_BUCKET_NAME`

into `settings_s3.example.py` and rename it to `settings_s3.py`. Your django
server can then be run with the command

    DJANGO_SETTINGS_MODULE=settings_s3 python manage.py runserver

**Recommended procedure**

1. Create IAM user specifically for Franklin
2. Create bucket for Franklin
3. Set up bucket policy
4. Set up CORS configuration (if needed)

### 1. Create IAM user
We recommend creating an IAM user under your account so that you don't access
the S3 bucket directly via the root user on your AWS account.  This can be done
under `Security Credentials` in the top right menu in the AWS Console.
Then select `Users` in the left side panel, and then `Create New Users`.

_Do not set permissions on the IAM user as a `User Policy` under `Security
Credentials` it will not work._

### 2. Create a bucket
In the standard S3 overview you can create a bucket by pressing the blue button
in the upper left. Choose your desired region and name.

### 3. Bucket policy
We then restrict permissions by setting up a bucket policy on the bucket.
This is done from the "Properties" pane on the right, in the standard S3 view.

While having the bucket selected, and showing the Properties pane, unfold
Permissions and press _Add bucket policy_ (or _Edit bucket policy_).

The final recommended bucket policy looks like this, and we recommend you copy
and paste this into the bucket policy textfield:

_Please replace AWS\_ACCOUNT\_ID, IAM\_USER, BUCKET\_NAME with the your actual AWS
Account Id, the name of the IAM user you created, and the bucket name,
respectively._

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "DjangoMediaControl",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::AWS_ACCOUNT_ID:user/IAM_USER"
                },
                "Action": [
                    "s3:AbortMultipartUpload",
                    "s3:ListBucket",
                    "s3:DeleteObject",
                    "s3:GetObject",
                    "s3:PutObjectAcl",
                    "s3:PutObjectVersionAcl",
                    "s3:ListBucketMultipartUploads",
                    "s3:ListMultipartUploadParts",
                    "s3:PutObject"
                ],
                "Resource": [
                    "arn:aws:s3:::BUCKET_NAME",
                    "arn:aws:s3:::BUCKET_NAME/*"
                ]
            },
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::BUCKET_NAME/*"
            }
        ]
    }

#### Explanation for the bucket policy

In order to download things from the bucket you need permissions to the actions:

    "Action": [
        "s3:GetObject",
        "s3:ListBucket"
    ],
    "Resource": [
        "arn:aws:s3:::gcl-images",
        "arn:aws:s3:::gcl-images/*"
    ]

As you can see in the `Resource` section you need to specify both the root of
the bucket (the bucket itself) and all files in it.

In order to upload things from the bucket you need permissions to the actions:

    "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:AbortMultipartUpload",
        "s3:ListBucketMultipartUploads",
        "s3:ListMultipartUploadParts",
        "s3:PutObjectAcl",
        "s3:PutObjectVersionAcl"
    ]

Fos static files hosting on S3 you also need the `s3:DeleteObject` permission.

### 4. CORS configuration
If your only django staticfiles consists of only images, css and javascript you
can skip this step. You can check your browser console for errors like
`Cross-Origin Request Blocked`. If you use fonts for example you need to change
the CORS configuration of the bucket.

Setting up CORS is done the same way as the bucket policy, only the _Edit CORS
Configuration_ button is right next to the _Edit Bucket Policy_ button.

_Change http://example.org to the domain where your Franklin instance is
hosted._

    <CORSConfiguration>
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
            <MaxAgeSeconds>3000</MaxAgeSeconds>
            <AllowedHeader>Authorization</AllowedHeader>
        </CORSRule>
        <CORSRule>
            <AllowedOrigin>http://example.org</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
           <AllowedHeader>*</AllowedHeader>
        </CORSRule>
    </CORSConfiguration>

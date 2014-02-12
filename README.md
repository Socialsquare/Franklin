Global Change Lab
=================
Global Change Lab is an activist training platform built by BIT BLUEPRINT and
Socialsquare for actionAid.

The readme contains section explaining how to configure different parts of the
project.

Getting started
---------------
You need to have [node](adfsdf)

If you don't already have `grunt` installed, install it:

    npm install -g grunt-cli

Install the node dependencies (package.json):

    npm install

Install the bower dependencies (bower.json):

    bower install

Database migrations (using South)
---------------------------------
Initially (when you start your project) you should run the following commands:

    > ./manage.py syncdb
    > ./manage.py schemamigration skills --initial
    > ./manage.py migrate skills

When you change your models the database will have to be updated.
You first create a migration

    > ./manage.py schemamigration skills --auto

And then apply it:

    > ./manage.py migrate skills

That's it! Good luck :o)

Amazon S3
---------
Global Change Lab uses Amazon S3 as backend image host (to save bandwidth costs).

I recommend creating an IAM user under your account so that you don't access the
S3 bucket directly via the root user on your AWS account.
_Do not set permissions on the IAM user as a `User Policy` under `Security
Credentials` it will not work._

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

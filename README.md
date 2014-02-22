Global Change Lab
=================
Global Change Lab is an activist training platform built by BIT BLUEPRINT and
Socialsquare for actionAid.

The readme contains section explaining how to configure different parts of the
project.

Getting started
---------------
If you haven't already set up a virtual environment please see the
**Virtual environment** section below.

Step 1. Install the needed Python packages by running this command:

    > pip install -r requirements.txt

Step 2. In order to build the site you need to have
[Node.js](http://nodejs.org/) installed. Depending on your setup and package
manager there will be different ways of doing this:

| OS X (with homebrew) | Arch               | Ubuntu, Mint             |
| -------------------- | ------------------ | ------------------------ |
| `brew install node`  | `pacman -S nodejs` | `apt-get install nodejs` |

Step 3. Then if you don't already have `grunt` installed, install it:

    > npm install -g grunt-cli

Step 4. Install the node dependencies (package.json):

    > npm install

Step 5. Build the project

    > grunt

Which does the following things:

* Installs the the bower dependencies (bower.json)
* Builds the CSS from SASS (.scss-files)

Step 6. django syncdb

    > python manage.py syncdb

Step 7. South migrations

    > python manage.py migrate

Step 8. Try it out!

    > python manage.py runserver

You should now be able to see the site at <http://localhost:8000> :)

### Virtual environment
We recommend setting up a virtual environment. It is not required but, it is
good practice.
If you don't already have virtualenv, install it with the command

    > pip install virtualenv

(You may need to `sudo` the above command)

Then create the virtual environment in the folder `.venv`:

    > virtualenv .venv

And lastly activate the virtual environment:

    > . .venv/bin/activate


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

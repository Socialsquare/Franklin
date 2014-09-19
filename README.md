Global Change Lab
=================
Global Change Lab is an activist training platform built by BIT BLUEPRINT and
Socialsquare for actionAid.

The readme contains section explaining how to configure different parts of the
project.

Getting started
---------------

Global Change Lab uses the 3.4+ version of the Python interpreter, make sure you have this installed before proceeding.

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
    
(optional) Step 9. Create a superuser

    > python manage.py createsuperuser

You should now be able to see the site at <http://localhost:8000> :)

### Virtual environment
We recommend setting up a virtual environment. It is not required but, it is
good practice.
If you don't already have virtualenv, install it with the command

    > pip install virtualenv

(You may need to `sudo` the above command)

Then create the virtual environment in the folder `.venv`:

    > virtualenv --python=python3.4 .venv

And lastly activate the virtual environment:

    > . .venv/bin/activate


Database migrations (using South)
---------------------------------
Initially (when you start your project) you should run the following commands:

    > ./manage.py syncdb
    > ./manage.py migrate skills
    > ./manage.py migrate

When you change your models the database will have to be updated.
You first create a migration

    > ./manage.py schemamigration skills --auto

And then apply it:

    > ./manage.py migrate skills

SQLite
------
For testing purposes you can enable an SQLite backend instead of the default
PostgreSQL. This is done by setting the environment variable `GCL_USE_SQLITE`.
If the varible is present in the environment (regardless of its value) a local
SQLite database in will be used. (Residing in the file `database.sqlite3`)

Tests
-----
You can run the tests by running the command

    python manage.py test global_change_lab.tests

By default the tests are run through Google Chrome.
You need to have the executable binary `chromedriver` on your `PATH`.
`chromedriver` can be downloaded [here](https://code.google.com/p/selenium/wiki/ChromeDriver).

You can also test with Mozilla Firefox by setting the environment variable
`FRANKLIN_TEST_FIREFOX`, e.g.

    FRANKLIN_TEST_FIREFOX=1 python manage.py test global_change_lab.tests

in this case you don't need the `chromedriver` binary.

### Running a single test
A single test from the test suite can be run with a command like this:

    python manage.py test global_change_lab.tests.SeleniumTestSuite.test_login

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

For static files hosting on S3 you also need the `s3:DeleteObject` permission.

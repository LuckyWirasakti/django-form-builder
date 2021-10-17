Introduction
==

This project is a simple skeleton to get you started with Django and Heroku.
It currently uses the stable release of Django 3.2.
The steps below should get you up and running quickly.

Deployment
==

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

The project is already set up for easy deployment with Heroku by clicking the button above.
Note that you will be warned if your account will be charged for the addons installed.
While I make no guarantees, I have attempted to select only free addons which leave room to upgrade.
You are still responsible for verifying any fees associated with any addons which will be installed.

For the first deploy, and each new deploy, simply run `git push heroku master`.
Initially, and when the schema changes, run `migrate`.

    heroku run python manage.py migrate

You can view your new deployment in your browser via `heroku open`.
Static file serving can be modified to use Amazon S3.
Create a bucket on S3 and add the configuration to your Heroku installation.

    heroku config:add AWS_ACCESS_KEY_ID="<AWS access key>"
    heroku config:add AWS_SECRET_ACCESS_KEY="<AWS secret>"
    heroku config:add AWS_STORAGE_BUCKET_NAME="<bucket name>"

If using S3, you will find `collectstatic` takes a long time to run on every deploy.
To disable running automatically, simply set `DISABLE_COLLECTSTATIC=1`.
You can then manually run `collectstatic` via

    heroku run python manage.py collectstatic --noinput


Dependency management
==

To add a new dependency to your project, simply install via `pip install` after activating the virtualenv.
To track newly installed packages, run `pip freeze -l > requirements.txt` to update the requirements file.
Note that you should manually remove `setuptools` or `distribute` if they appear in this file as this can cause slug compilation to fail.

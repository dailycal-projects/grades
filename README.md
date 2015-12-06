# Grades

Parse and explore UC Berkeley grade distribution data from [Cal Answers](http://calanswers.berkeley.edu/).

## Requirements

Python 2.7.x, Postgres, and the packages in `requirements.txt`.

## Setup

Create a new virtualenv and clone the repository.
```
virtualenv grades
git clone https://github.com/dailycal-projects/grades.git
```
Create a Postgres database. For example, if you wanted to call it `grades`:
```
createdb grades
```
Set the following environment variables using `EXPORT VARIABLE = 'VALUE'`:
  * `DJANGO_SECRET_KEY`: a secret key (usually a randomly generated string)
  * `DJANGO_SETTINGS_MODULE`: use `ucbgradedists.settings.local` if you're in a development environment, and `ucbgradedists.settings.production` in production.
  * `DATABASE_URL`: a URL to your database. See the [dj_database_url](https://github.com/kennethreitz/dj-database-url) README for the format.
  * `ADMIN_NAME`, `ADMIN_EMAIL`: a name and email for the admin of the site.
  * `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: Gmail user and password for the email to send from.
  * `SERVER_EMAIL`: the email that the server should send emails from (to admins/managers).
 
Migrate the database.
```
python manage.py migrate
```

Run a series of management commands to import data and compute statistics. These can be run in succession with a meta-command.
```
python manage.py setup
```
This will call:
* `python manage.py import_dir [dir]` to import data from all CSV files in a directory.
* `python manage.py import_disciplines` to import a mapping of subjects to academic disciplines.
* `python manage.py compute_stats` to compute statistics.

## License

This project is covered by the MIT License in `LICENSE.txt`.

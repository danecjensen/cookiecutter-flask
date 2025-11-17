# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description}}

## Docker Quickstart

This app can be run completely using `Docker` and `docker compose`. **Using Docker is recommended, as it guarantees the application is run using compatible versions of Python and Node**.

There are three main services:

To run the development version of the app

```bash
docker compose up flask-dev
```

To run the production version of the app

```bash
docker compose up flask-prod
```

The list of `environment:` variables in the `docker compose.yml` file takes precedence over any variables specified in `.env`.

To run any commands using the `Flask CLI`

```bash
docker compose run --rm manage <<COMMAND>>
```

Therefore, to initialize a database you would run

```bash
docker compose run --rm manage db init
docker compose run --rm manage db migrate
docker compose run --rm manage db upgrade
```

A docker volume `node-modules` is created to store NPM packages and is reused across the dev and prod versions of the application. For the purposes of DB testing with `sqlite`, the file `dev.db` is mounted to all containers. This volume mount should be removed from `docker compose.yml` if a production DB server is used.

Go to `http://localhost:8080`. You will see a pretty welcome screen.

### Running locally

Run the following commands to bootstrap your environment if you are unable to run the application using Docker

```bash
cd {{cookiecutter.app_name}}
{%- if cookiecutter.use_pipenv == "True" %}
pipenv install --dev
pipenv shell
{%- else %}
pip install -r requirements/dev.txt
{%- endif %}
npm install
npm run-script build
npm start  # run the webpack dev server and flask server using concurrently
```

Go to `http://localhost:5000`. You will see a pretty welcome screen.

#### Database Initialization (locally)

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration

```bash
flask db init
flask db migrate
flask db upgrade
```

## Deployment

When using Docker, reasonable production defaults are set in `docker compose.yml`

```text
FLASK_ENV=production
FLASK_DEBUG=0
```

Therefore, starting the app in "production" mode is as simple as

```bash
docker compose up flask-prod
```

If running without Docker

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
export DATABASE_URL="<YOUR DATABASE URL>"
npm run build   # build assets with webpack
flask run       # start the flask server
```

### Deploying to Render.com

This template includes configuration files for easy deployment to [Render.com](https://render.com/). Render automatically provides:

- Free PostgreSQL database (with limitations on free tier)
- Free web service with 750 hours/month
- Automatic deployments from Git
- Free SSL certificates

**Prerequisites:**
- A [Render.com account](https://dashboard.render.com/register)
- Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)

**Deployment Steps:**

1. **Push your code to a Git repository** (if not already done)

2. **Add migrations to version control**
   ```bash
   git add migrations/*
   git commit -m "Add migrations"
   ```

3. **Create a new Blueprint on Render**
   - Go to your [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" and select "Blueprint"
   - Connect your Git repository
   - Render will automatically detect the `render.yaml` file

4. **Configure environment variables** (if needed)
   - Render will auto-generate a `SECRET_KEY`
   - The `DATABASE_URL` is automatically configured to use the PostgreSQL database
   - You can add custom environment variables in the Render dashboard

5. **Deploy**
   - Render will automatically build and deploy your application
   - The build process runs `render_build.sh` which:
     - Installs Python dependencies
     - Installs Node.js dependencies and builds assets
     - Runs database migrations

6. **Access your application**
   - Once deployed, your app will be available at: `https://{{cookiecutter.app_name}}.onrender.com`
   - The free tier may spin down after inactivity; first request may take 30-60 seconds

**Manual Deployment (Alternative):**

If you prefer not to use the Blueprint, you can manually create services:

1. Create a PostgreSQL database in Render
2. Create a Web Service in Render with these settings:
   - **Runtime**: Python 3
   - **Build Command**: `./render_build.sh`
   - **Start Command**: `gunicorn {{cookiecutter.app_name}}.app:create_app() -b 0.0.0.0:$PORT -w 3`
   - **Environment Variables**: Link the database and set `FLASK_APP`, `FLASK_ENV`, `SECRET_KEY`

**Important Notes:**
- The free PostgreSQL database on Render has a 1GB storage limit and will expire after 90 days
- Consider upgrading to a paid plan for production applications
- Database backups are only available on paid plans

## Shell

To open the interactive shell, run

```bash
docker compose run --rm manage shell
flask shell # If running locally without Docker
```

By default, you will have access to the flask `app`.

## Running Tests/Linter

To run all tests, run

```bash
docker compose run --rm manage test
flask test # If running locally without Docker
```

To run the linter, run

```bash
docker compose run --rm manage lint
flask lint # If running locally without Docker
```

The `lint` command will attempt to fix any linting/style errors in the code. If you only want to know if the code will pass CI and do not wish for the linter to make changes, add the `--check` argument.

## Migrations

Whenever a database migration needs to be made. Run the following commands

```bash
docker compose run --rm manage db migrate
flask db migrate # If running locally without Docker
```

This will generate a new migration script. Then run

```bash
docker compose run --rm manage db upgrade
flask db upgrade # If running locally without Docker
```

To apply the migration.

For a full migration command reference, run `docker compose run --rm manage db --help`.

If you will deploy your application remotely (e.g on Heroku) you should add the `migrations` folder to version control.
You can do this after `flask db migrate` by running the following commands

```bash
git add migrations/*
git commit -m "Add migrations"
```

Make sure folder `migrations/versions` is not empty.

## Asset Management

Files placed inside the `assets` directory and its subdirectories
(excluding `js` and `css`) will be copied by webpack's
`file-loader` into the `static/build` directory. In production, the plugin
`Flask-Static-Digest` zips the webpack content and tags them with a MD5 hash.
As a result, you must use the `static_url_for` function when including static content,
as it resolves the correct file name, including the MD5 hash.
For example

```html
<link rel="shortcut icon" href="{{ "{{" }}static_url_for('static', filename='build/favicon.ico') {{ "}}" }}">
```

If all of your static files are managed this way, then their filenames will change whenever their
contents do, and you can ask Flask to tell web browsers that they
should cache all your assets forever by including the following line
in ``.env``:

```text
SEND_FILE_MAX_AGE_DEFAULT=31556926  # one year
```

{%- if cookiecutter.use_heroku == "True" %}

## Heroku

Before deploying to Heroku you should be familiar with the basic concepts of [Git](https://git-scm.com/) and [Heroku](https://heroku.com/).

Remember to add migrations to your repository. Please check `Migrations`_ section.

Since the filesystem on Heroku is ephemeral, non-version controlled files (like a SQLite database) will be lost at least once every 24 hours. Therefore, a persistent, standalone database like PostgreSQL is recommended. This application will work with any database backend that is compatible with SQLAlchemy, but we provide specific instructions for Postgres, (including the required library `psycopg2-binary`).

**Note:** `psycopg2-binary` package is a practical choice for development and testing but in production it is advised to use the package built from sources. Read more in the [psycopg2 documentation](http://initd.org/psycopg/docs/install.html?highlight=production%20advised%20use%20package%20built%20from%20sources#binary-install-from-pypi).

If you keep your project on GitHub you can use 'Deploy to Heroku' button thanks to which the deployment can be done in web browser with minimal configuration required.
The configuration used by the button is stored in `app.json` file.

<a href="https://heroku.com/deploy" style="display: block"><img src="https://www.herokucdn.com/deploy/button.svg" title="Deploy" alt="Deploy"></a>
    <br>

Deployment by using [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli):

* Create Heroku App. You can leave your app name, change it, or leave it blank (random name will be generated)

    ```bash
    heroku create {{cookiecutter.app_name}}
    ```

* Add buildpacks

    ```bash
    heroku buildpacks:add --index=1 heroku/nodejs
    heroku buildpacks:add --index=1 heroku/python
    ```

* Add database addon which creates a persistent PostgresSQL database. These instructions assume you're using the free [hobby-dev](https://elements.heroku.com/addons/heroku-postgresql#hobby-dev) plan. This command also sets a `DATABASE_URL` environmental variable that your app will use to communicate with the DB.

    ```bash
    heroku addons:create heroku-postgresql:hobby-dev --version=11
    ```

* Set environmental variables (change `SECRET_KEY` value)

    ```bash
    heroku config:set SECRET_KEY=not-so-secret
    heroku config:set FLASK_APP=autoapp.py
    heroku config:set SEND_FILE_MAX_AGE_DEFAULT=31556926
    ```

* Please check `.env.example` to see which environmental variables are used in the project and also need to be set. The exception is `DATABASE_URL`, which Heroku sets automatically.

* Deploy on Heroku by pushing to the `heroku` branch

    ```bash
    git push heroku main
    ```

{%- endif %}

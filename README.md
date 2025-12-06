# resume-builder

This repository contains a Django-based resume builder app.

## Quick start (macOS / zsh)

Follow these steps to create a virtual environment, install dependencies, run migrations, and start the development server.

1. Open a terminal and change to the project directory:
   
    git clone https://github.com/sivaprakashDesingu/resume-builder.git
   
	cd resume-builder

3. Create a virtual environment (recommended name: `.venv`):

	python3 -m venv .venv

4. Activate the virtual environment:

	source .venv/bin/activate

5. Upgrade pip and install dependencies. This project does not include a `requirements.txt` file by default; at minimum install Django 4.x (the project was generated with Django 4.x):

	python -m pip install --upgrade pip setuptools wheel
	pip install "django>=4,<5"

	If you later create a `requirements.txt`, install with:

	pip install -r requirements.txt

6. Apply database migrations:

	python manage.py migrate

7. Start the development server (default port 8000):

	python manage.py runserver 127.0.0.1:8000

	If you prefer to run the server without activating the venv shell, run the venv python directly:

	.venv/bin/python manage.py runserver 127.0.0.1:8000

8. Open your browser at http://127.0.0.1:8000/ to view the site.

## Notes & troubleshooting

- If port 8000 is already in use, either stop the other process or run the server on a different port, e.g. `python manage.py runserver 127.0.0.1:8001`.
- If you see "Couldn't import Django" when running management commands, ensure your virtualenv is activated and Django is installed in it.
- To capture exact installed packages for future installs, run:

  pip freeze > requirements.txt

- Database: the project uses SQLite by default and the file `db.sqlite3` is included in the repo. No further DB setup should be required for development.

## Adding a requirements.txt (recommended)

After you have a working venv with all required packages installed, export them:

  pip freeze > requirements.txt

Commit `requirements.txt` so other developers can reproduce your env with `pip install -r requirements.txt`.

## Contact / Next steps

If you want, I can:

- generate a `requirements.txt` from the current venv and add it to the repo,
- add a small `Makefile` or npm-style scripts for convenience,
- or add Docker support to run the app in a container.

Happy hacking!

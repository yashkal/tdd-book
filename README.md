# Obey the Testing Goat!

This repository contains my work from the [TDD for Python
book](https://www.obeythetestinggoat.com/pages/book.html).
There are a couple of things that I do differently in my work that I list below.
These changes are for practicing tools and techniques that I think will make me
more productive in building services in the long run.

- `makefile` to organize code and reduce unneccesary typing
- `pytest` instead of Django test client
- `docker` for provisioning and deployment (see `deployment_notes.md`)

## Getting Started (DEV)

Create virtual environment and install necessary packages.

```
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r app/requirements-dev.txt
```

Also need to add `geckodriver`.

```
brew install geckodriver    # Or use whatever package manager for your OS
```

## Makefile

The `makefile` provides targets that simplifies development process. Simply run
`make` or `make help` to view available targets.

```
make build  # Build container images
make run    # Run containers (detached mode)
make logs   # View container logs
make test   # Run unit and functional tests
make clean  # Stop and remove running containers
```

To rebuild, test, and clean up environment, use the following one-liner. The
environment will not clean itself if there are any errors in testing. If this
happens, the containers will still be running for debugging.

```
make rebuild run test clean
```

# Solfilm

You must use Pipenv to run the script and manage the dependencies with Pipfile.

* https://github.com/pypa/pipenv

To run:

```bash
pipenv shell
python src/generate.py
```

To run inside Docker:

```bash
docker build -t solfilm .
docker run --rm solfilm:latest python ./src/generate.py
```

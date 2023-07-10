# Pytest examples

## Requirements

* **python >3.5**
* **docker**

## Get started

### Prepare environment

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run tests

#### Default run

```shell
pytest .
```
#### Verbose run

```shell
pytest -vvv .
```

#### Run with specific redis

```shell
pytest -vvv --redis-version 6.2 --redis-version 7.0 .
```

#### Run slow tests

```shell
pytest -vvv --run-slow .
```

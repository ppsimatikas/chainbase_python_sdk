![](docs/logo.png)

## A python SDK connecting you with the big blockchain data !

This python SDK is build to accelerate your development efforts in getting data from the big blockchains, by utilizing Chainbase's powerful data infrastructure.
See the docs [here](https://docs.chainbase.com/docs) 

## How do I install this SDK?

To install this python Chainbase from the Python Package Index (PyPI) run:

```
pip install chainbase_sdk
```

## What are the main features of this SDK?

| Feature              | What is this?                                                                       | API Reference                                               |
| -------------------- |-------------------------------------------------------------------------------------|-------------------------------------------------------------|
| SQL | Run low-latency SQL queries against all our indexed datasets for your custom needs. | [link](https://docs.chainbase.com/reference/data-cloud-sql) |

## How do I use the Chainbase SDK?

First you need to setup the `CHAINBASE_API_KEY` environment variable, or pass it as parameter in `Chainbase('[api-key]')`.

Follow the steps below to obtain your API key:

1. Go to the [Chainbase console](https://console.chainbase.com/)
2. Under `Dashboard`
3. Select existing project or `New Project`
4. Copy the `API Key`.

```
from chainbase_sdk import Chainbase

client = Chainbase()

df = client.sql.query_pandas("select * from ethereum.blocks limit 10")
print(df)
```

See more under [examples](./examples)

## Local development

1. Clone: `git clone`
2. `cd ./chainbase_python_sdk`
3. `make install_dev`

## How to install dependencies

Declare any dependencies in `requirements.txt` for production and `requirements_dev.txt` for development.

To install them, run:

For production:
```
make install
```

For development:
```
make install_dev
```

## How to test your project

All test files are under [examples](./tests). You can run your tests:

```
make test
```

This will also run coverage.

## How to check your code formatting

This project is using [black](https://black.readthedocs.io/en/stable/), [flake8](https://flake8.pycqa.org/en/latest/) and [isort](https://pycqa.github.io/isort/) to keep coding formatting standards.

To format your code run: 

```
make format 
```

To check your code formatting:

```
make lint 
```

## How to verify your code

Verifying your project requires all the lint formatting to pass and tests to pass.
You can run the command bellow to execute:

```
make verify 
```




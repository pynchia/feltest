# Inventory management system


## Setup and execution of the tests

`docker build --target pybuild -t testbuild .`

`docker run -it testbuild`

## Setup and execution of the backend

Go to the root `feltest` directory and build the docker image

`docker build -t appbuild .`

Launch it

`docker run -it -p 8000:8000 appbuild`

## Web access to frontend

Point your browser to:

- `http://localhost:8000/`
to use the web interface

- `http://localhost:8000/`
to enjoy the  REST API documentation DRF generates automatically


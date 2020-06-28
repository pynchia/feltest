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

## Assumptions

A batch contains N items of the same product, e.g. 1000 packets of Pilau rice

## Data model

Product:
	name
	supplier
	weight
	# price

Batch:
	product(fk on Product)  # which product
	pur_date  # purchased on
	exp_date  # expires on
	init_qty  # initial quantity
	curr_qty  # current quantity
	tot_cost  # paid for the batch

BatchEvents:
	batch(fk on Batch)  # to which batch it refers
	ev_date  # when it occurred
	ev_type  # ADD, SUB

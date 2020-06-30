#!/bin/bash
pytest -s --cov=inventory/ --cov-report html --cov-report annotate

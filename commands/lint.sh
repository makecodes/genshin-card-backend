#!/bin/bash
flake8 .
black --check .
isort --check-only .

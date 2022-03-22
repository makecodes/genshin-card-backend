#!/bin/bash

/bin/bash ./commands/wait-for-it.sh "${DB_HOST}:${DB_PORT}" --timeout=90 --strict -- pytest
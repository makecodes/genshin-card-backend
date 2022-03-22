#!/bin/bash

/bin/bash /home/makecodes/commands/wait-for-it.sh "${DB_HOST}:${DB_PORT}" --timeout=90 --strict -- pytest

#!/bin/sh
celery -A app worker -l INFO --concurrency=2 -Q ${QUEUE_NAME}

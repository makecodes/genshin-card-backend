FROM python:3.8-buster as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

RUN apt-get update && apt-get install -y \
    bash \
    build-essential \
    default-libmysqlclient-dev \
    libmariadb-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    python3-dev \
    libxml2-dev \
    libxslt-dev && \
    apt-get install -y --no-install-recommends gcc && \
    pip install -U pip

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    C_FORCE_ROOT=true

# Create and switch to a new user
RUN useradd --create-home makecodes
WORKDIR /home/makecodes
USER makecodes

# Install application into container
COPY . .

CMD ["/home/makecodes/commands/run-prod.sh"]

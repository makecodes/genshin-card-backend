import os

import newrelic.agent
from datadog import initialize, statsd
from django.conf import settings

initialize(**{"statsd_host": settings.DATADOG_HOST, "statsd_port": settings.DATADOG_PORT})


def _process_tags(tags):
    """
    Format a dict with tags to the format expected by datadogpy.
    For example:
    {
        "foo": "bar",
        "baz": "quux"
    }
    Translates to: ["foo:bar", "baz:quux"]
    Args:
        tags (dict or None): a dictionary of "tag name": "tag value" items, or None.
    Returns:
        list: tags as expected by datadogpy.
    """
    base_tags = {"scope": os.getenv("SCOPE", "production")}

    _tags = tags or {}
    _tags.update(base_tags)
    return ["{}:{}".format(tag, value) for tag, value in _tags.items()]


def record_count(name, increment=1, tags=None):
    """
    Counters track how many times something happens per second.
    Implemented as Datadog Counter (https://docs.datadoghq.com/developers/metrics/counts/).
    Args:
        name (str): metric name.
        increment (int, optional): The counter is incremented by this given value.
            Defaults to 1.
        tags (dict, optional): Dictionary of "tag name": "tag value" items.
            Defaults to None.
    """
    name = f"{settings.DATADOG_APP_PREFIX}{name}"
    statsd.increment(name, increment, tags=_process_tags(tags))


def record_gauge(name, value, tags=None):
    """
    Gauges measure the value of a particular thing over time.
    They are implemented as [Datadog Gauges](https://docs.datadoghq.com/developers/metrics/gauges/)
    Args:
        name (str): metric name.
        value (number): value to record for the flush interval.
        tags (dict, optional): Dictionary of "tag name": "tag value" items. Defaults to None.
    """
    name = f"{settings.DATADOG_APP_PREFIX}{name}"
    statsd.gauge(name, value, tags=_process_tags(tags))


def record_histogram(name, value, tags=None):
    """
    Histograms measure the statistical distribution of a set of values.
    They are implemented as Datadog Histograms
    https://docs.datadoghq.com/developers/metrics/histograms/
    For a metric named `my_metric`, the following metrics are generated:
    `my_metric.avg`, `my_metric.count`, `my_metric.median`, `my_metric.95percentile`,
    `my_metric.max` and `my_metric.min`
    Args:
        name (str): metric name.
        value (number): The value to add to the distribution computation.
        tags (dict, optional): Dictionary of "tag name": "tag value" items. Defaults to None.
    """
    name = f"{settings.DATADOG_APP_PREFIX}{name}"
    statsd.histogram(name, value, tags=_process_tags(tags))


def newrelic_event(event_type, tags):
    _tags = _process_tags(tags)
    newrelic.agent.record_custom_event(event_type, _tags)

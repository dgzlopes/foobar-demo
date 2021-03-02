from flask import Flask
from flask import request
from opentracing.ext import tags
from opentracing.propagation import Format
from jaeger_client import Config
from time import sleep
import random
from opentracing.ext import tags
from opentracing.propagation import Format
import requests


def init_tracer(service):
    config = Config(
        config={"sampler": {"type": "const", "param": 1,}, "logging": True,},
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


app = Flask(__name__)
tracer = init_tracer("service-foo")


def http_get(span, port, path):
    url = f"http://localhost:{port}/{path}"

    span.set_tag(tags.HTTP_METHOD, "GET")
    span.set_tag(tags.HTTP_URL, url)
    span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
    headers = {}
    tracer.inject(span, Format.HTTP_HEADERS, headers)

    r = requests.get(url, headers=headers)
    return r.text


@app.route("/foo")
def foo():
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
    with tracer.start_active_span("foo", child_of=span_ctx, tags=span_tags) as span:
        span.span.log_kv({"example": "some interesting information", "count": 124})
        span.span.set_tag("type", "important-for-the-demo")
        with tracer.start_span("call-bar", child_of=span.span) as bar:
            return "foo" + http_get(bar, 8084, "/bar")


if __name__ == "__main__":
    app.run(port=8083)

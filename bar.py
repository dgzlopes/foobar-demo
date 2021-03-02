from time import sleep
from flask import Flask
from flask import request
from opentracing.ext import tags
from opentracing.propagation import Format
from jaeger_client import Config

# :)
# import random


def init_tracer(service):
    config = Config(
        config={"sampler": {"type": "const", "param": 1,}, "logging": True,},
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


app = Flask(__name__)
tracer = init_tracer("service-bar")


def expensive_calculation(n):
    if n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return expensive_calculation(n - 1) + expensive_calculation(n - 2)


@app.route("/bar")
def bar():
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
    with tracer.start_active_span("bar", child_of=span_ctx, tags=span_tags) as span:
        with tracer.start_span("expensive-calculation", child_of=span.span):
            expensive_calculation(random.randint(1, 10))
        return "bar"


if __name__ == "__main__":
    app.run(port=8084)

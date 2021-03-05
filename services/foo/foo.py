from flask import Flask, request
import requests
from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="service-foo",
    # configure agent
    agent_host_name="otel-collector",
    agent_port=6831,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchExportSpanProcessor(jaeger_exporter)
)

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


@app.route("/foo")
def foo():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("bar-request"):
        r = requests.get("http://bar:5000/bar")
    return "foo" + r.text


if __name__ == "__main__":
    app.run(port=8083)

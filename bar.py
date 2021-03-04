from time import sleep
from flask import Flask, request
from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="service-bar",
    # configure agent
    agent_host_name="localhost",
    agent_port=6831,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchExportSpanProcessor(jaeger_exporter)
)

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)


@app.route("/bar")
def bar():
    return "bar"


if __name__ == "__main__":
    app.run(port=8084)

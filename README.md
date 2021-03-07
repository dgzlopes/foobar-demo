## foobar

This is a distributed tracing demo! Foobar consists of two **extremely** complex services: foo and bar.

On this demo:
- You can generate load with k6.
- Services foo and bar:
  - Are written in Python.
  - Are instrumented with OpenTelemetry.
  - Export the spans to an OpenTelemetry Collector using the Jaeger exporter.
- The OpenTelemetry Collector exports the tracing data to Grafana Tempo.
- Grafana Tempo can be queried from Grafana.

Here's a small diagram:
<p align="center">
<img src="media/diagram.png" alt="diagram" />
</p>

## QuickStart

Requirements: Docker, Docker Compose, and k6.

1. Build and run services with docker-compose:
```
docker-compose up --build -d 
```

2. See running services with:
```
docker-compose ps
```

3. Generate some load with k6:
```
k6 run example.js
```

4. See logs with:
```
docker-compose logs foo bar
```

5. Pick a `trace_id` from the logs.

6. Go to Grafana (http://localhost:3000) -> Explore -> Tempo and paste the `trace_id`.

7. Stop the whole setup with:
```
docker-compose stop
```


## FooBar

Run services:

```
# one terminal
python foo.py
# another terminal
python bar.py
```

## Jaeger

Run Jaeger:
```
docker run -d --name demo \
  -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 14250:14250 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.22
```

Go to Jaeger UI:

http://localhost:16686

Remove Jaeger:

```
docker stop demo; docker rm demo
```


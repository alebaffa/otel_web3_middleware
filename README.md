## OpenTelemetry middleware for Web3

This is a working example of how to track Web3 calls with Opentelemetry.

### Setup and run

- install and run Jaeger: `make start/jaeger` (it will download the official Docker image and run it)
- install the virtual environment: `python3.11 -m venv env`
- activate it: `. venv/bin/activate`
- install dependencies: `make setup`
- run the program: `make start`

### Open Jaeger

Open your browser to `[http://localhost:16686](http://localhost:16686/)` to see the traces in Jaeger.
You should see the traces like
![](otel-test.png)

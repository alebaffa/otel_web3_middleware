from typing import Any, Callable

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from web3.main import AsyncWeb3
from web3.types import AsyncMiddlewareCoroutine, RPCEndpoint


def init_tracer() -> None:
    resource = Resource.create({"service.name": "Web3 otel example"})
    tracer_provider = TracerProvider(resource=resource)
    set_global_textmap(TraceContextTextMapPropagator())
    tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(tracer_provider)


async def otel_web3_middleware(
    make_request: Callable[[RPCEndpoint, Any], Any], async_w3: "AsyncWeb3"
) -> AsyncMiddlewareCoroutine:
    async def middleware(method: RPCEndpoint, params: Any) -> Any:
        tracer = trace.get_tracer(__package__)
        with tracer.start_as_current_span(f"web3.{method}"):
            for i, param in enumerate(params):
                trace.get_current_span().set_attribute(str(i), str(param))

            return await make_request(method, params)

    return middleware

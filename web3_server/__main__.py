import asyncio
import os

from opentelemetry import trace

from middleware.otel import init_tracer
from middleware.web3 import get_web3


async def main():
    # Instantiate Web3
    web3 = get_web3()

    with trace.get_tracer(__package__).start_as_current_span(
        "My application",
    ):
        # Perform eth_call
        await web3.eth.call(
            {
                "value": 0,
                "gas": 21736,
                "maxFeePerGas": 15254192295,
                "maxPriorityFeePerGas": 1000000000,
                "to": "0xc305c901078781C232A2a521C2aF7980f8385ee9",
                "data": "0x477a5c98",
            }
        )

        await web3.eth.get_balance("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")


if __name__ == "__main__":
    init_tracer()
    asyncio.run(main())

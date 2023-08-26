import threading
from typing import cast

from web3 import AsyncWeb3
from web3._utils.caching import generate_cache_key
from web3.middleware import async_construct_simple_cache_middleware
from web3.types import RPCEndpoint

from middleware.otel import otel_web3_middleware


def get_web3() -> AsyncWeb3:
    w3 = AsyncWeb3(
        AsyncWeb3.AsyncHTTPProvider(
            "https://mainnet.infura.io/v3/<your-api-key>"
        ),
        # middleware=[] <-- you can also pass custom middlewares here, but this will override the default ones. Be careful.
    )

    async def _async_simple_cache(make_request, async_w3):
        middleware = await async_construct_simple_cache_middleware(
            rpc_whitelist={RPCEndpoint("eth_chainId")},
        )
        return await middleware(make_request, async_w3)

    w3.middleware_onion.add(_async_simple_cache, name="Cache chain_id")
    w3.middleware_onion.add(otel_web3_middleware)

    return w3

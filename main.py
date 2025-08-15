import os
import logging
import time
import asyncio
from dotenv import load_dotenv
from binance_sdk_derivatives_trading_usds_futures.derivatives_trading_usds_futures import (
    DerivativesTradingUsdsFutures,
    ConfigurationRestAPI,
    DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL,
)
from binance_sdk_derivatives_trading_usds_futures.rest_api.models import (
    NewOrderSideEnum,
    NewOrderTimeInForceEnum,
)


# load_dotenv(".env")


# Configure logging
logging.basicConfig(level=logging.INFO)

# Create configuration for the REST API
configuration_rest_api = ConfigurationRestAPI(
    api_key=os.getenv("BINANCE_API_KEY", ""),
    api_secret=os.getenv("BINANCE_API_SECRET", ""),
    base_path=os.getenv(
        "BINANCE_BASE_PATH", DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL
    ),
)


client = DerivativesTradingUsdsFutures(config_rest_api=configuration_rest_api)


async def new_order():
    while True:
        await asyncio.sleep(10)

        try:
            start_time = time.time()

            response = client.rest_api.new_order(
                symbol="BTCUSDT",
                side=NewOrderSideEnum["BUY"].value,
                type="LIMIT",
                time_in_force=NewOrderTimeInForceEnum["GTC"].value,
                quantity=0.1,
                price=10000,  # impossible price on 2025/08/15
            )

            end_time = time.time()
            logging.info(f"new_order() time: {(end_time - start_time)*1000:.2f} ms")

            rate_limits = response.rate_limits
            logging.info(f"new_order() rate limits: {rate_limits}")

            data = response.data()
            logging.info(f"new_order() response: {data}")
        except Exception as e:
            logging.error(f"new_order() error: {e}")

            end_time = time.time()
            logging.info(f"new_order() time: {(end_time - start_time)*1000:.2f} ms")


if __name__ == "__main__":
    asyncio.run(new_order())

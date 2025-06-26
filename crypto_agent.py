import asyncio
import httpx

BINANCE_ALL_COINS_URL = "https://api.binance.com/api/v3/ticker/price"
BINANCE_COIN_BY_SYMBOL_URL = "https://api.binance.com/api/v3/ticker/price?symbol={}"


class CryptoAgent:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def get_all_coin_rates(self):
        try:
            response = await self.client.get(BINANCE_ALL_COINS_URL)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            return f"❌ Network error: {e}"
        except httpx.HTTPStatusError as e:
            return f"❌ HTTP error: {e.response.status_code}"

    async def get_coin_rate_by_symbol(self, symbol: str):
        url = BINANCE_COIN_BY_SYMBOL_URL.format(symbol.upper())
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            return f"✅ {data['symbol']} rate: {data['price']}"
        except httpx.HTTPStatusError:
            return f"❌ Symbol '{symbol}' not found or invalid."
        except httpx.RequestError as e:
            return f"❌ Network error: {e}"

    async def close(self):
        await self.client.aclose()


async def main():
    agent = CryptoAgent()

    print("\n🚀 Welcome to the Realtime Crypto Rate Agent. By Muhammad Samad!\n")
    print("🔹 Type 'all' to see all coin rates")
    print("🔹 Type any coin symbol like 'BTCUSDT', 'ETHUSDT', etc.")
    print("🔹 Type 'exit' to quit\n")

    while True:
        user_input = input("🔍 Enter symbol or 'all': ").strip()
        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "all":
            all_rates = await agent.get_all_coin_rates()
            if isinstance(all_rates, str):
                print(all_rates)
            else:
                for coin in all_rates[:10]:
                    print(f"{coin['symbol']}: {coin['price']}")
                print(f"...and {len(all_rates) - 10} more.")
        else:
            result = await agent.get_coin_rate_by_symbol(user_input)
            print(result)

    await agent.close()
    print("👋 Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import aiohttp
from pytoniq import LiteClient
from pytoniq_core import Address

async def fetch_balance(url, params=None, json=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, json=json) as response:
            if response.status == 200:
                return await response.json()
            return None

async def balance_via_toncenter(address: str) -> str:
    url = "https://toncenter.com/api/v2/getAddressBalance"
    data = await fetch_balance(url, params={"address": address})
    return data.get("result", "Failed to get balance.") if data else "Error while getting balance."

async def balance_via_tonhub(address: str) -> str:
    url = "https://mainnet.tonhubapi.com/getAddressBalance"
    data = await fetch_balance(url, params={"address": address})
    return data.get("result", "Failed to get balance.") if data else "Error while getting balance."

async def balance_via_tonapi(address: str) -> str:
    url = f"https://tonapi.io/v2/accounts/{Address(address).to_str()}"
    data = await fetch_balance(url)
    return data.get("balance", "Failed to get balance.") if data else "Error while getting balance."

async def balance_via_anton(address: str) -> str:
    url = "https://anton.tools/api/v0/accounts"
    params = {
        "address": address,
        "latest": "true",
        "order": "DESC",
        "count": "false"
    }
    data = await fetch_balance(url, params=params)
    if data and "results" in data and data['results']:
        return data['results'][0].get('balance', "Failed to get balance.")
    return "Error while getting balance."

async def balance_via_dton(address: str) -> str:
    endpoint = 'https://dton.io/graphql/'
    query = f'''
    {{
        raw_account_states(
        address__friendly: "{address}"
        ) {{
            account_storage_balance_grams
            }}
        }}
    '''
    data = await fetch_balance(endpoint, json={'query': query})
    if data and "data" in data and data['data']['raw_account_states']:
        balance = data['data']['raw_account_states'][0].get('account_storage_balance_grams', "Failed to get balance.")
        return str(int(balance)) if isinstance(balance, (float, int)) else balance
    return "Error while getting balance."

async def balance_via_toncenter_v3(address: str) -> str:
    url = "https://toncenter.com/api/v3/account"
    data = await fetch_balance(url, params={"address": address})
    return data.get("balance", "Failed to get balance.") if data else "Error while getting balance."

async def balance_via_litesever(address: str) -> str:
    async with LiteClient.from_mainnet_config(ls_i=7, trust_level=2) as client:
        result = await client.get_account_state(address)
        return result.balance

async def main():
    address = "UQD4z7hHo5XS8OcAUHrZ7YpODVpfZI4eja182c9aPpa2TUHP"

    tasks = {
        "toncenter": balance_via_toncenter(address),
        "tonhub": balance_via_tonhub(address),
        "tonapi": balance_via_tonapi(address),
        "anton": balance_via_anton(address),
        "dton": balance_via_dton(address),
        "toncenter v3": balance_via_toncenter_v3(address),
        "litesever": balance_via_litesever(address)
    }

    for name, task in tasks.items():
        try:
            balance = await task
            print(f"{name}: {balance}")
        except Exception as e:
            print(f"{name}: Failed to retrieve balance due to {e}")

asyncio.run(main())
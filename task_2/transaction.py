import asyncio
from pytoniq import LiteBalancer, WalletV4R2, begin_cell, Address
from pytoniq_core import WalletMessage
from seed import mnemo

async def transfer():
    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:
        wallet = await WalletV4R2.from_mnemonic(client, mnemo)
        print(wallet, wallet.balance)

        body = (begin_cell()
                .store_uint(0x706c7567, 32)
                .end_cell())

        msg = wallet.create_wallet_internal_message(
            destination=Address("kQBOrhNyLCPNnt7MUVxJVUSEUQF6_10q7plprvRwCiqYhJF9"),
            send_mode=17,
            value=1 * 10 ** 7,
            body=body
        )

        await wallet.raw_transfer(msgs=[msg])

asyncio.run(transfer())
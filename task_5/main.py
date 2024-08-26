import asyncio

from bitstring import BitArray
from pytoniq import LiteBalancer, WalletV4R2, begin_cell
from pytoniq_core.crypto.keys import mnemonic_new

async def get_wallet_address(client: LiteBalancer, jetton_address: str, user_address: str):
    cs = begin_cell().store_address(user_address).to_slice()
    result = await client.run_get_method(jetton_address, 'get_wallet_address', [cs])
    return result[0].load_address()

async def main():
    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:
        while True:
            wallet = await WalletV4R2.from_mnemonic(client, mnemonic_new())
            addr = wallet.address
            addr_pfx = BitArray(hex=addr.hash_part.hex()).bin[:4]

            jetton_wallet = await get_wallet_address(
                client=client,
                jetton_address='EQDI4tLpoDYtLwfC_HEaI6TroiyPQ8NbGl1smxwm4ehByFQt',
                user_address=addr.to_str()
            )
            jetton_wallet_pfx = BitArray(hex=jetton_wallet.hash_part.hex()).bin[:4]

            if addr_pfx == '0000' and jetton_wallet_pfx == '0000':
                print(f'Address: {addr}, ', f' {BitArray(hex=addr.hash_part.hex()).bin}')
                print(f'Jetton wallet: {jetton_wallet}, ', f' {BitArray(hex=jetton_wallet.hash_part.hex()).bin}')
                break

        print(addr)


asyncio.run(main())
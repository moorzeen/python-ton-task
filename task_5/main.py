import asyncio

from bitstring import BitArray
from pytoniq import LiteBalancer, WalletV4R2
from pytoniq_core.crypto.keys import mnemonic_new


def get_prefix(binary_string: str) -> str:
    reversed_binary = binary_string[::-1]
    first_1_index_reversed = reversed_binary.find('1') + 1
    prefix_reversed = reversed_binary[first_1_index_reversed:]
    return prefix_reversed[::-1]

async def main():
    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:
        while True:
            wallet = await WalletV4R2.from_mnemonic(client, mnemonic_new())
            addr = wallet.address
            addr_pfx = BitArray(hex=addr.hash_part.hex()).bin[:4]
            if addr_pfx == '0000':
                print(f'Address: {addr}')
                break

asyncio.run(main())
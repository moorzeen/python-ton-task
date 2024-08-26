import asyncio

from bitstring import BitArray
from pytoniq import LiteBalancer, Address, Transaction, BlockId, Block
from pytoniq.liteclient.sync import get_last_stored_blocks


def get_prefix(binary_string: str) -> str:
    reversed_binary = binary_string[::-1]
    first_1_index_reversed = reversed_binary.find('1') + 1
    prefix_reversed = reversed_binary[first_1_index_reversed:]
    return prefix_reversed[::-1]

async def main():
    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:

        shards = await client.get_all_shards_info()

        pfx_len = 4
        for i, shard in enumerate(shards):
            shard_bin = BitArray(int=shards[i].shard, length=64).bin
            if len(get_prefix(shard_bin)) < pfx_len:
                pfx_len = len(get_prefix(shard_bin))
                break

        address = Address('UQD4z7hHo5XS8OcAUHrZ7YpODVpfZI4eja182c9aPpa2TUHP')
        address_pfx = BitArray(hex=address.hash_part.hex()).bin[:pfx_len]

        for shard in shards:
            shard_bin = BitArray(int=shard.shard, length=64).bin
            if get_prefix(shard_bin) == address_pfx:
                print('Current account shard: ', BitArray(bin=shard_bin).hex)
                break

        trx, ids = await client.raw_get_transactions(address, count=1)
        print(ids[0])

asyncio.run(main())
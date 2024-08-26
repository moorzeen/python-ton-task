import asyncio

from bitstring import BitArray
from pytoniq import LiteBalancer, Address, ShardIdent

def get_prefix(binary_string: str) -> str:
    reversed_binary_string = binary_string[::-1]
    first_1_index_reversed = reversed_binary_string.find('1') + 1
    prefix_reversed = reversed_binary_string[first_1_index_reversed:]
    return prefix_reversed[::-1]

async def main():
    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:

        shards = await client.get_all_shards_info()

        shard_bin = BitArray(int=shards[0].shard, length=64).bin
        pfx_len = len(get_prefix(shard_bin))

        address = Address('UQD4z7hHo5XS8OcAUHrZ7YpODVpfZI4eja182c9aPpa2TUHP')
        address_pfx = BitArray(hex=address.hash_part.hex()).bin[:pfx_len]

        for shard in shards:
            shard_bin = BitArray(int=shard.shard, length=64).bin
            if get_prefix(shard_bin) == address_pfx:
                print(BitArray(bin=shard_bin).hex)

asyncio.run(main())
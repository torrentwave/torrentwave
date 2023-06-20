import asyncio
from pydht import DHT

async def crawl_torrent_info(info_hash):
    dht = DHT()

    async with dht:
        await dht.bootstrap()

        # Look up the torrent info in the DHT
        peers = await dht.get_peers(info_hash)
        torrent_metadata = await dht.get_metadata(info_hash)

        print("Torrent Info:")
        print("Info Hash:", info_hash)
        print("Peers:", peers)
        print("Metadata:", torrent_metadata)

    await dht.stop()

if __name__ == "__main__":
    info_hash = "690539bb2f3ab573543d2db3a50cf32a1e5cce45"  # Replace with your desired info hash

    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawl_torrent_info(info_hash))

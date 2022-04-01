import asyncio
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from anchorpy import Program, Provider, Wallet


async def main():
    client = AsyncClient("https://api.mainnet-beta.solana.com/")
    provider = Provider(client, Wallet.local())
    # load the Serum Swap Program (not the Serum dex itself).
    program_id = PublicKey("22Y43yTVxuUkoRKdm9thyRhQ3SdgQS7c7kB6UNCiaczD")
    # load the Mango DEX program Id - it does have no IDL at blockchain
    # program_id = PublicKey("mv3ekLzLbnVPNxjSKvqBpU3ZeZXPQdEC3bp5MDEBG68")
    try:
        program = await Program.at(
            program_id, provider
        )
        print(program.idl.name)  # swap

        f = open("/tmp/program-idl.txt", "w")
        f.write(str(program.idl))
        f.close()
    finally:
        await program.close()


asyncio.run(main())
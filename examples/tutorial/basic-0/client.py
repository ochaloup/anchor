import logging

from pathlib import Path
import asyncio
import json
from solana.publickey import PublicKey
from anchorpy import Idl, Program

logging.basicConfig(level=logging.INFO)

async def main():
    # Read the generated IDL.
    with Path("target/idl/basic_0.json").open() as f:
        raw_idl = json.load(f)
    idl = Idl.from_json(raw_idl)

    # Address of the deployed program.
    program_id = PublicKey("7RJ7c3E3rxFD3NScPVssfKk5psBVXEWjQBwPdex2DACE")

    # Generate the program client from IDL.
    # context manager closes the http client in background what is needed
    async with Program(idl, program_id) as program:
        # Execute the RPC.
        logging.info(f"Running program {program_id}")
        await program.rpc["initialize"]()
        logging.info(f"Program {program_id} was run sucesfully")

asyncio.run(main())
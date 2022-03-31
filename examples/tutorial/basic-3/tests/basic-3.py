# tests/basic-0.py
import asyncio
import typing
from pytest import fixture, mark
from solana.keypair import Keypair
from anchorpy import (
    create_workspace, close_workspace, Context, Program
)
from solana.system_program import SYS_PROGRAM_ID

# see
# https://kevinheavey.github.io/anchorpy/testing/

@fixture(scope="module")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@fixture(scope="module")
async def program_puppet() -> Program:
    workspace = create_workspace()
    yield workspace["puppet"]
    await close_workspace(workspace)

@fixture(scope="module")
async def program_puppet_master() -> Program:
    workspace = create_workspace()
    yield workspace["puppet_master"]
    await close_workspace(workspace)


@mark.asyncio
async def test_puppet_cpi_call(
    program_puppet_master: Program, program_puppet: Program
) -> None:
    puppet_data_account = Keypair()
    await program_puppet.rpc["initialize"](
        ctx=Context(
            accounts={
                "puppet": puppet_data_account.public_key,
                "user": program_puppet.provider.wallet.public_key,
                "system_program": SYS_PROGRAM_ID,
            },
            signers=[puppet_data_account],
        ),
    )
    puppet_account = await program_puppet.account["Data"].fetch(puppet_data_account.public_key)
    assert puppet_account.data == 0

    await program_puppet_master.rpc["pull_strings"](
        42,
        ctx=Context(
            accounts={
                "puppet": puppet_data_account.public_key,
                "puppet_program": program_puppet.program_id
            }
        ),
    )
    puppet_account = await program_puppet.account["Data"].fetch(puppet_data_account.public_key)
    assert puppet_account.data == 42

# tests/basic-0.py
import asyncio
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
async def program() -> Program:
    workspace = create_workspace()
    yield workspace["basic_1"]
    await close_workspace(workspace)

@fixture(scope="module")
async def initialized_account(program: Program) -> Keypair:
    my_account = Keypair()
    await program.rpc["initialize"](
        1234,
        ctx=Context(
            accounts={
                "my_account": my_account.public_key,
                "user": program.provider.wallet.public_key,
                "system_program": SYS_PROGRAM_ID,
            },
            signers=[my_account],
        ),
    )
    return my_account


@mark.asyncio
async def test_is_initialized(
    program: Program, initialized_account: Keypair
) -> None:
    account = await program.account["MyAccount"].fetch(initialized_account.public_key)
    assert account.data == 1234


@mark.asyncio
async def test_update(
    program: Program, initialized_account: Keypair
) -> None:
    await program.rpc["update"](
        2222, ctx=Context(accounts={"my_account": initialized_account.public_key})
    )
    account = await program.account["MyAccount"].fetch(initialized_account.public_key)
    assert account.data == 2222
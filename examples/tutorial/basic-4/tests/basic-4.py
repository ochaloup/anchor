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
async def secured_account_program() -> Program:
    workspace = create_workspace()
    yield workspace["basic_4"]
    await close_workspace(workspace)


@mark.asyncio
async def test_secured_account(
    secured_account_program: Program
) -> None:
    data_account_keypair = Keypair()
    # THIS DOES NOT WORK and I do not know how to access the AnchorPy in version 0.23.0 basic-4
    # the program IDL contains 'state' and I don't know how to make it callable
    print(f'>>>> {secured_account_program.idl.state.methods}')
    new_method_list = list(filter(lambda p : p.name == 'new', secured_account_program.idl.state.methods))
    new_method = new_method_list[0] if len(new_method_list) == 1 else None
    print(f'>>>> {new_method} // _IdlInstruction')
    await new_method(
        ctx=Context(
            accounts={
                "authority": secured_account_program.provider.wallet.public_key
            },
            signers=[data_account_keypair],
        ),
    )
    secured_account = await secured_account_program.account["Auth"].fetch(data_account_keypair.public_key)
    assert secured_account.count == 0
    assert secured_account.authority == secured_account_program.provider.wallet.public_key

    await secured_account_program.rpc["increment"](
        ctx=Context(
            accounts={
                "authority": secured_account_program.provider.wallet.public_key
            }
        ),
    )
    secured_account = await secured_account_program.account["Auth"].fetch(data_account_keypair.public_key)
    assert secured_account.count == 1
    assert secured_account.authority == secured_account_program.provider.wallet.public_key

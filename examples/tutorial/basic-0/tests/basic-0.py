# tests/basic-0.py
import asyncio
from pytest import fixture, mark
from anchorpy import create_workspace, close_workspace, Program


# Since our other fixtures have module scope, we need to define
# this event_loop fixture and give it module scope otherwise
# pytest-asyncio will break.

@fixture(scope="module")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture(scope="module")
async def program() -> Program:
    workspace = create_workspace()
    yield workspace["basic_0"]
    await close_workspace(workspace)

@mark.asyncio
async def test_initialize(
    program: Program
) -> None:
    await program.rpc["initialize"]()
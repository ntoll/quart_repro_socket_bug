import pytest


@pytest.fixture(name="app", scope="function")
async def _app():
    from my_app.app import app
    await app.startup()
    yield app
    await app.shutdown()


@pytest.mark.asyncio
async def test_websocket(app):
    client = app.test_client()
    async with client.session_transaction() as local_session:
        local_session["user_id"] = "1"
    async with client.websocket("/ws") as test_websocket:
        await test_websocket.send("ping")
        result = await test_websocket.receive()
        assert result == "ping"

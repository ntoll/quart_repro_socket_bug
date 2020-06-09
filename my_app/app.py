from quart import Quart, session, websocket, abort, current_app
from functools import wraps


app = Quart(__name__)

app.config.update(
    {
        "SECRET_KEY": "veryverysecret",
    }
)


def require_user(func):
    """
    A decorator for websocket connections.

    Ensure the user_id is in the session. Otherwise, abort the connection.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if user_id:
            return await func(*args, **kwargs)
        else:
            abort(401)

    return wrapper


@app.route("/", methods=["GET"])
async def client():
    """
    Get something from session.
    """
    if session.get("user_id"):
        return "It works"
    else:
        abort(404)


@app.websocket("/ws")
@require_user
async def ws():
    # This code will never run in the tests.
    while True:
        data = await websocket.receive()
        await websocket.send(data)

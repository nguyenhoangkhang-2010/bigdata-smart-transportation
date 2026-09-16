from backend.app.core.redis import get_redis_client


def test_redis_connection():
    client = get_redis_client()

    assert client.ping() is True
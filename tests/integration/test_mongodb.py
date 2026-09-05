from backend.app.core.mongodb import get_mongo_client, get_mongo_database


def test_mongodb_connection():
    client = get_mongo_client()

    result = client.admin.command("ping")

    assert result["ok"] == 1.0


def test_mongodb_database():
    database = get_mongo_database()

    assert database.name == "smart_transportation"
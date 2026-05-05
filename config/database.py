"""
config/database.py
Async MongoDB connection via Motor.
"""

import motor.motor_asyncio
from config.settings import settings

_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)
db      = _client.get_default_database()


async def connect_db():
    """Ping the database to confirm connection on startup."""
    await _client.admin.command("ping")
    print(f"[DB] Connected to MongoDB: {settings.MONGODB_URI}")


async def close_db():
    _client.close()
    print("[DB] MongoDB connection closed.")

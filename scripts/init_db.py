"""
Database initialization script.
Verifies connection, createspgvector extension if missing, and runs initial migrations.
"""

import asyncio
from sqlalchemy import text
from packages.database.session import engine


async def init_database() -> None:
    """Verifies connection and initializes pgvector extension."""
    print("Connecting to database...")
    async with engine.begin() as conn:
        print("Creating pgvector extension if not exists...")
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        print("pgvector extension initialized successfully.")
    await engine.dispose()
    print("Database initialization complete.")


if __name__ == "__main__":
    asyncio.run(init_database())

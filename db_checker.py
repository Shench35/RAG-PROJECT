import asyncio
import traceback
from sqlalchemy.ext.asyncio import create_async_engine
from src.app.services.config import Config

async def test_conn():
    print(f"DEBUG: DATABASE_URL is: '{Config.DATABASE_URL}'")
    
    # Check if the URL is still the placeholder
    if "user:password" in Config.DATABASE_URL:
        print("❌ ERROR: You are still using the placeholder 'user:password'. Please check your .env file.")
        return

    try:
        # We'll try to connect with a 10-second timeout
        # For Neon, we often need to ensure SSL is handled correctly by the driver
        engine = create_async_engine(
            Config.DATABASE_URL,
            connect_args={"ssl": True} if "ssl=require" in Config.DATABASE_URL or "neon.tech" in Config.DATABASE_URL else {}
        )
        
        print("Attempting to connect...")
        async with engine.connect() as conn:
            print("✅ SUCCESS: Successfully connected to Neon PostgreSQL!")
            
    except Exception:
        print("❌ CONNECTION FAILED")
        print("-" * 30)
        traceback.print_exc()
        print("-" * 30)
    finally:
        if 'engine' in locals():
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_conn())

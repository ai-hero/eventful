import os
import pymongo
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
import traceback

CONNECTION_URL = os.environ["CONNECTION_URL"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
CLIENT: AsyncIOMotorClient = AsyncIOMotorClient(CONNECTION_URL)
DB: AsyncIOMotorDatabase = CLIENT[DATABASE_NAME]


def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    return DB[collection_name]


def retry(num_tries, exceptions):
    def decorator(func):
        def f_retry(*args, **kwargs):
            for _ in range(num_tries):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    traceback.print_exc()
                    continue

        return f_retry

    return decorator


# Retry on AutoReconnect exception, maximum 3 times
retry_auto_reconnect = retry(3, (pymongo.errors.AutoReconnect,))

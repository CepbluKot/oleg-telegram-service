import asyncio
from api import get_connection_data, init_session


connection_data = get_connection_data()
session = asyncio.run(init_session)

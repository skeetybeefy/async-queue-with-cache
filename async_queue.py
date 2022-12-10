import asyncio

counter = 0
threshold = 2
timeout = 3

queue = asyncio.Queue(maxsize=10)
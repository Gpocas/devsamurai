import httpx
import aiofiles 
from shutil import copyfileobj

client = httpx.AsyncClient()

async def get_binary(url: str):
    async with client.stream('GET', url) as response:
        async for chunk in response.aiter_bytes():
            yield chunk

async def save_file(content: bytes, filename: str) -> None:
    async with aiofiles.open('teste.zip', 'wb') as f:
        await copyfileobj(content, f)
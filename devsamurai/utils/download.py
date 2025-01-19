import asyncio
import httpx
import aiofiles
from rich.progress import Progress
from devsamurai.utils.settings import Settings
from devsamurai.utils.csv_utils import update_csv

s = Settings()

client = httpx.AsyncClient(http2=True, timeout=20)

async def download_and_save(
    url: str,
    filename: str,
    progress: Progress,
    task_id: int,
    semaphore: asyncio.Semaphore,
    row: dict,
) -> None:
    async with semaphore:
        async with client.stream('GET', url) as response:
            total = int(response.headers.get('Content-Length', 0))
            progress.update(task_id, total=total)

            async with aiofiles.open(filename, 'wb') as f:
                async for chunk in response.aiter_bytes():
                    await f.write(chunk)
                    progress.update(task_id, advance=len(chunk))

            progress.remove_task(task_id)
            row['status'] = 'completed'
            update_csv(row)



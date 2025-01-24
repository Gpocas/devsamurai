import asyncio
from niquests import AsyncSession, Response
import aiofiles
from rich.progress import Progress
from devsamurai.utils.settings import Settings
from devsamurai.utils.csv_utils import update_csv

s = Settings()

async def niquests_download_and_save(
    url: str,
    filename: str,
    progress: Progress,
    task_id: int,
    semaphore: asyncio.Semaphore,
    row: dict,
) -> None:
    async with semaphore:
        async with AsyncSession(disable_http1=True) as client:
            response: Response = await client.get(url, stream=True)
            total = int(response.headers.get('Content-Length', 0))
            progress.update(task_id, total=total)

            async with aiofiles.open(filename, 'wb') as f:
                async for chunk in await response.iter_content():
                   await f.write(chunk)
                   progress.update(task_id, advance=len(chunk))

            progress.remove_task(task_id)
            row['status'] = 'completed'
            update_csv(row)

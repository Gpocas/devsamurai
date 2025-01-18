import asyncio
import httpx
import aiofiles
from rich.progress import Progress

client = httpx.AsyncClient()


async def download_and_save(
    url: str, filename: str, progress: Progress, task_id: int
) -> None:
    async with client.stream('GET', url) as response:
        total = int(response.headers.get('Content-Length', 0))
        progress.update(task_id, total=total)

        async with aiofiles.open(filename, 'wb') as f:
            async for chunk in response.aiter_bytes():
                await f.write(chunk)
                progress.update(task_id, advance=len(chunk))


if __name__ == '__main__':
    url = r'https://cursos.devsamurai.com.br/Aulas%20ao%20Vivo.zip'
    filename = 'video.zip'
    progress = Progress()
    task_id = progress.add_task('Downloading', total=0)

    with progress:
        asyncio.run(download_and_save(url, filename, progress, task_id))

import asyncio
import httpx
import aiofiles
from rich.progress import Progress

client = httpx.AsyncClient(http2=True, timeout=20)


async def download_and_save(
    url: str,
    filename: str,
    progress: Progress,
    task_id: int,
    semaphore: asyncio.Semaphore,
) -> None:
    async with semaphore:
        async with client.stream('GET', url) as response:
            total = int(response.headers.get('Content-Length', 0))
            progress.update(task_id, total=total)

            async with aiofiles.open(filename, 'wb') as f:
                async for chunk in response.aiter_bytes():
                    await f.write(chunk)
                    progress.update(task_id, advance=len(chunk))

            # Remove task from progress when complete
            progress.remove_task(task_id)


if __name__ == '__main__':
    url = r'https://cursos.devsamurai.com.br/Aulas%20ao%20Vivo.zip'
    filename = 'video.zip'
    progress = Progress()
    task_id = progress.add_task('Downloading', total=0)

    with progress:
        asyncio.run(
            download_and_save(
                url, filename, progress, task_id, asyncio.Semaphore(10)
            )
        )

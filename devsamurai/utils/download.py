import asyncio
import csv
import httpx
import aiofiles
from rich.progress import Progress
from devsamurai.utils.settings import Settings

s = Settings()

client = httpx.AsyncClient(http2=True, timeout=20)


async def download_and_save(
    url: str,
    filename: str,
    progress: Progress,
    task_id: int,
    semaphore: asyncio.Semaphore,
    csv_file_path: str,
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

            # Remove task from progress when complete
            progress.remove_task(task_id)
            row['status'] = 'completed'
            update_csv(csv_file_path, row)


def update_csv(csv_file_path: str, updated_row: dict) -> None:
    rows = []
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            if row['name'] == updated_row['name']:
                row['status'] = updated_row['status']
            rows.append(row)

    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, delimiter=';', quotechar='"'
        )
        writer.writeheader()
        writer.writerows(rows)


def delete_failed_download(csv_file_path: str):
    rows = []
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            if row.get('status') != 'completed':
                rows.append(row.get('name'))

    for file in s.DOWNLOAD_PATH.iterdir():
        if file.stem in rows:
            file.unlink()

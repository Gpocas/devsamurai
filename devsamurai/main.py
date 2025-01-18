import asyncio
import csv
from pathlib import Path
from rich.progress import Progress
from devsamurai.utils import download_and_save, Settings

s = Settings()

if not s.DOWNLOADS_PATH.exists():
    s.DOWNLOADS_PATH.mkdir()


async def main():
    tasks = []
    csv_file_path = s.CSV_PATH

    progress = Progress()
    with progress:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                url = row['url']
                filename = str(s.DOWNLOADS_PATH / row['name']) + '.zip'
                task_id = progress.add_task(
                    f'Downloading {row["name"]}', start=False
                )
                tasks.append(
                    download_and_save(url, filename, progress, task_id)
                )

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())

import asyncio
import csv
from shutil import rmtree
from rich.progress import Progress
from devsamurai.utils import download_and_save, Settings

s = Settings()

if not s.DOWNLOAD_PATH.exists():
    s.DOWNLOAD_PATH.mkdir()
else:
    rmtree(s.DOWNLOAD_PATH)
    s.DOWNLOAD_PATH.mkdir(exist_ok=True)


async def main():
    tasks = []
    csv_file_path = s.CSV_PATH
    semaphore = asyncio.Semaphore(10)  # Limitar para 10 tarefas simultâneas

    progress = Progress()
    with progress:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                url = row['url']
                filename = str(s.DOWNLOAD_PATH / row['name']) + '.zip'
                task_id = progress.add_task(
                    f'Downloading {row["name"]}', start=False
                )
                tasks.append(
                    download_and_save(
                        url, filename, progress, task_id, semaphore
                    )
                )

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())

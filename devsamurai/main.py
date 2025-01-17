import asyncio
import csv
from pathlib import Path
from rich.progress import Progress
from devsamurai.utils.download import download_and_save

BASE_PATH = Path(__file__).resolve().parent.parent
DOWNLOADS_PATH = BASE_PATH / 'downloads'

if not DOWNLOADS_PATH.exists():
    DOWNLOADS_PATH.mkdir()

async def main():
    tasks = []
    csv_file_path = BASE_PATH / 'aulas.csv'
    
    progress = Progress()
    with progress:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                url = row['url']
                filename = str(DOWNLOADS_PATH / row['name']) + '.zip'
                task_id = progress.add_task(f"Downloading {row['name']}", start=False)
                tasks.append(download_and_save(url, filename, progress, task_id))
        
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())




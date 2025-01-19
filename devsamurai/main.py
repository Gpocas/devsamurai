import asyncio
import csv
import time
import rich
from rich.progress import Progress, BarColumn
from devsamurai.utils import download_and_save, Settings

s = Settings()

if not s.DOWNLOAD_PATH.exists():
    s.DOWNLOAD_PATH.mkdir()


async def main():
    tasks = []
    csv_file_path = s.CSV_PATH
    semaphore = asyncio.Semaphore(s.PARALLEL_DOWNLOADS)
    progress = Progress(
        '[progress.description]{task.description}',
        BarColumn(),
        '[progress.percentage]{task.percentage:>3.1f}%',
        '•',
        '[progress.filesize]{task.completed}/{task.total}',
    )

    with progress:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                if row.get('status') == 'completed':
                    continue

                url = row['url']
                filename = str(s.DOWNLOAD_PATH / row['name']) + '.zip'
                task_id = progress.add_task(
                    f'Downloading {row["name"]}', start=True
                )
                tasks.append(
                    download_and_save(
                        url,
                        filename,
                        progress,
                        task_id,
                        semaphore,
                        csv_file_path,
                        row,
                    )
                )

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    total_time = end_time - start_time

    print('\n')
    print('*' * 50)
    rich.print(
        f'[green]• [white]Tempo total de execução: [blue]{total_time:.2f} [white]segundos'
    )
    print('*' * 50)

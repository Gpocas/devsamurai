import csv
from devsamurai.utils.settings import Settings

s = Settings()

def update_csv(updated_row: dict) -> None:
    rows = []
    with open(s.CSV_PATH, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            if row['name'] == updated_row['name']:
                row['status'] = updated_row['status']
            rows.append(row)

    with open(s.CSV_PATH, 'w', newline='') as csvfile:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, delimiter=';', quotechar='"'
        )
        writer.writeheader()
        writer.writerows(rows)


def delete_failed_download():
    rows = []
    with open(s.CSV_PATH, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            if row.get('status') != 'completed':
                rows.append(row.get('name'))

    for file in s.DOWNLOAD_PATH.iterdir():
        if file.stem in rows:
            file.unlink()
import gspread
from bdfile import select_all_staff
import gspread
from oauth2client.service_account import ServiceAccountCredentials




def update_sheet(worker_name, date, start_time, duration_hours):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('cleanproject-421520-c6e6efde7a68.json', scope)
    client = gspread.authorize(credentials)


    sheet = client.open('cleantable').sheet1


    date_range = sheet.range('B4:BD4')
    time_range = sheet.range('B5:BD5')
    worker_range = sheet.range('A6:A')


    date_column_index = None
    for index, cell in enumerate(date_range):
        if cell.value == date:
            date_column_index = index
            break

    if date_column_index is None:
        return


    time_row_index = None
    if len(start_time) == 5 and start_time[0] == '0':
        start_time = start_time[1:]
    for index, cell in enumerate(time_range):
        if cell.value == start_time:
            time_row_index = index
            break

    if time_row_index is None:
        return

    worker_row_index = None
    for index, cell in enumerate(worker_range):
        if cell.value == worker_name:
            worker_row_index = index + 6
            break

    if worker_row_index is None:
        return

    cells_to_update = []

    for i in range(duration_hours):
        cell_row = worker_row_index
        cell_column = date_column_index + 2 + i
        cell_row_index = time_row_index
        cell = sheet.cell(cell_row, cell_column + cell_row_index)
        cell.value = 'занят'
        cell.format = {
            "backgroundColor": {
                "red": 1.0,
                "green": 0.0,
                "blue": 0.0
            },
            "textFormat": {
                "foregroundColor": {
                    "red": 1.0,
                    "green": 1.0,
                    "blue": 1.0
                }
            }
        }

        cell.format = cell.format
        cells_to_update.append(cell)
    sheet.update_cells(cells_to_update)
    print(
        f"Таблица успешно обновлена для работника {worker_name} на дату {date} с {start_time} на {duration_hours} часов.")



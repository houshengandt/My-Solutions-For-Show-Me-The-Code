import xlwt
import json


with open('city.txt', 'rb') as f:
    text = f.read().decode()
text_json = json.loads(text)
text_dict = sorted(text_json.items())

wb = xlwt.Workbook()
ws = wb.add_sheet('city')
row = 0
col = 0
for key, value in text_dict:
    ws.write(row, col, key)
    col += 1
    ws.write(row, col, value)
    row += 1
    col = 0

wb.save('city.xls')
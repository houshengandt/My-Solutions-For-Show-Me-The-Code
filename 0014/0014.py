import xlwt
import json


wb = xlwt.Workbook()
ws = wb.add_sheet('student')
with open('student.txt', 'rb') as f:
    text = f.read().decode()

text_json = json.loads(text)
text_dict = sorted(text_json.items())

row = 0
col = 0
for key, values in text_dict:
    ws.write(row, col, key)
    col += 1
    for i in values:
        ws.write(row, col, i)
        col += 1
    row += 1
    col = 0
wb.save('student.xls')

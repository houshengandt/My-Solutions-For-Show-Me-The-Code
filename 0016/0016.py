import xlwt
import json


with open('numbers.txt', 'rb') as f:
    text = f.read().decode()

text_json = json.loads(text)

wb = xlwt.Workbook()
ws = wb.add_sheet('numbers')
for i in range(0, len(text_json)):
    for j in range(0, len(text_json[i])):
        ws.write(i, j, text_json[i][j])
wb.save('numbers.xls')

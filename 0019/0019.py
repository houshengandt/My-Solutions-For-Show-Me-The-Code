from lxml import etree
import xlrd
import json


data = xlrd.open_workbook('numbers.xls')
table = data.sheet_by_index(0)
info = []
for i in range(table.nrows):
    numbers = []
    for j in range(table.ncols):
        numbers.append(table.row_values(i)[j])
    info.append(numbers)

root = etree.Element('root')
numbers = etree.SubElement(root, 'numbers')
numbers.append(etree.Comment('数字信息'))
numbers.text = json.dumps(info, ensure_ascii=True)
numbers_xml = etree.ElementTree(root)
numbers_xml.write('numbers.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
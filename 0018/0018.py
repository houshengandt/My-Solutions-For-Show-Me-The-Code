from lxml import etree
import xlrd
import json


data = xlrd.open_workbook('city.xls')
table = data.sheet_by_index(0)
info = {}
for i in range(table.nrows):
    info[str(table.row_values(i)[0])] = table.row_values(i)[1]

root = etree.Element('root')
cities = etree.SubElement(root, 'cities')
cities.append(etree.Comment('城市信息'))
cities.text = json.dumps(info, ensure_ascii=False)
cities_xml = etree.ElementTree(root)
cities_xml.write('cities.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')

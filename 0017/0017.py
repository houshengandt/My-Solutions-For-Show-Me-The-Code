import xlrd
import json
from lxml import etree


data = xlrd.open_workbook('student.xls')
table = data.sheet_by_index(0)
info = {}
for i in range(table.nrows):
    info[table.row_values(i)[0]] = table.row_values(i)[1:]

root = etree.Element('root')
students = etree.SubElement(root, 'students')
students.append(etree.Comment(u"""学生信息表 "id" : [名字, 数学, 语文, 英文]"""))
students.text = json.dumps(info, ensure_ascii=False)
student_xml = etree.ElementTree(root)
student_xml.write('students.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')


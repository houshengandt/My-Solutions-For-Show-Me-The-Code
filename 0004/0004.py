import re


with open('text.txt', 'rb') as f:
    text = str(f.read())


results = re.findall('[a-zA-Z0-9]+', text)
print(len(results))

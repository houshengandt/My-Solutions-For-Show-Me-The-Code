import re
import os
from collections import Counter


if os.path.isdir('diary'):
    for root, dirs, files in os.walk('diary'):
        for file in files:
            datalist = []
            filename = os.path.join('diary', file)
            with open(filename, 'r') as f:
                for line in f:
                    content = re.sub("\"|,|\.", "", line)
                    datalist.extend(content.strip().split(" "))
            counter = Counter(datalist)
            del counter['a']
            del counter['to']
            del counter['is']
            del counter['are']
            del counter['the']
            del counter['or']
            del counter['of']
            del counter['in']
            print(file + str(counter.most_common(3)))

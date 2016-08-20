import uuid


with open('key.txt', 'w') as f:
    for i in range(200):
        keys = str(uuid.uuid4())
        f.writelines(keys + '\n')

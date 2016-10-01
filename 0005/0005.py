import os
from fnmatch import fnmatch
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True  # 这个不加会有错误OSError: image file is truncated，还可以用StringIO解决


filenames = [name for name in os.listdir('pics') if fnmatch(name, '*.jpg')]
for filename in filenames:
    print(filename)
    fn = 'pics/' + filename
    f = Image.open(fn)
    x, y = f.size
    if(x > 1136) or (y > 640):
        if x > 1136:
            x_resize = 1136
            y_resize = int(1366/x*y)
        if y > 640:
            y_resize = 640
            x_resize = int(x*y_resize/y)
        f_iphone5 = f.resize((x_resize, y_resize))
        f_iphone5.save('pics_iphone5/' + filename)

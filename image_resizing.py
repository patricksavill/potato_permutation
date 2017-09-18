import os
from PIL import Image  # attainable via 'pip install pillow'

size = (512, 512)

# assuming the picture directory exists next to this script
for potato_image in os.listdir('Potatos'):
    try:
        im = Image.open('Potatos' + '/' + potato_image)
        re_im = im.resize(size, Image.BICUBIC)
        rgb_re_im = re_im.convert('RGB')

        DIR = "resized_potatos"
        if not os.path.exists(DIR):
            os.mkdir(DIR)

        rgb_re_im.save(DIR + '/' + 're+' + potato_image)
    except:
        print 'ruh roh: ' + potato_image
        # Some of the image scrubbing failed, so sadly errors need to be caught universally

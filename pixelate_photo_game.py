import glob
from PIL import Image
import requests
from io import BytesIO
from codetiming import Timer
import copy
import pathlib
import os

# Variables
workingdir = os.getcwd()
DURATION = 2100
RESOLUTIONS =  [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 32, 64, 128, 256, 312]



def create_animated_gif(idir, name="animated", suffix=".png", keep_intermediate_files=False):
    '''
    Takes all images of given suffix and creates animated gifs. Intermediate files are deleted
    '''
    # https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
    # filepaths
    fp_in = f"{idir}/*{suffix}"
    fp_out = f"{idir}/{name}.gif"
    sorted_input_files = sorted(glob.glob(fp_in))
    #print(sorted_input_files)
    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img, *imgs = [Image.open(f) for f in sorted_input_files]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
            save_all=True, duration=DURATION, loop=0)
    if keep_intermediate_files is False:
        for ifile in sorted_input_files:
            os.remove(ifile)


@Timer(name="decorator")
def pixelate_image(resolutions=[8,16,32,64,256,512]):
    # thanks https://stackoverflow.com/questions/47143332/how-to-pixelate-a-square-image-to-256-big-pixels-with-python
    
    for i in resolutions:
        # Resize smoothly down to new x,x pixels
        imgSmall = img.resize((i,i),resample=Image.BILINEAR)

        # Scale back up using NEAREST to original size
        result = imgSmall.resize(img.size,Image.NEAREST)

        # Save
        result.save(f'{resolutions.index(i):03d}_{i}_result.png')

# dictionary of photo name and url
d = {
    "green_leaf" : "https://cdn.stocksnap.io/img-thumbs/960w/green-leaf_BVKZ4QW8LS.jpg",
    "violett_flower"  : "https://cdn.stocksnap.io/img-thumbs/960w/pink-flower_EMV0UG5YO6.jpg",
    "city_woman" : "https://cdn.stocksnap.io/img-thumbs/960w/urban-woman_8RTGL25EL8.jpg",
    "firework"   : "https://cdn.stocksnap.io/img-thumbs/960w/fireworks-celebration_MGV2HJCQXT.jpg",
    "donots" : "https://cdn.stocksnap.io/img-thumbs/960w/doughnuts-plate_TG3ECHB0QY.jpg",
}

if __name__ == "__main__":
    for photo in d.keys():
        print(f"Processing {photo}")
        url = d[photo]
        response = requests.get(url) 
        img = Image.open(BytesIO(response.content))    
        
        pixelate_image(resolutions=RESOLUTIONS)
        create_animated_gif(idir=workingdir, name=photo)
       
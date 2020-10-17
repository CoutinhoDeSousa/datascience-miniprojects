## Imports

import argparse
import cv2
import pandas as pd
#declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

## getting imagepath from argument

ap = argparse.ArgumentParser()
ap.add_argument('-i','--image', required=True,
                help='Path of the Image')
args = vars(ap.parse_args())
imgpath = args['image']

######## Functions
# get x,y pos of mouse click
def draw_function(event, x,y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global  b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)


# calc distance to all colors and choose min
def getColorName(r,g,b):
    minimum = 1000000 ## just set it big
    for i in range(len(csv)):
        d = abs(r- int(csv.loc[i,'R']))
        + abs(g - int(csv.loc[i,'G']))
        + abs(b - int(csv.loc[i,'B']))
        if d<minimum:
            minimum = d
            cname = csv.loc[i,'color-name']
    return cname


### Read img with openc

img = cv2.imread(imgpath)

## Read the csv File
#generate index for file
#air_force_blue_raf,"Air Force Blue (Raf)",#5d8aa8,93,138,168

index = ['color','color-name','hex','R','G','B']
csv = pd.read_csv('colors.csv', names=index, header=None )

## Create a Window to display the image
cv2.namedWindow('image')
## Create mouse callback
cv2.setMouseCallback('image',draw_function)


### Listen for double clicks:
while(1):
    cv2.imshow('image',img)
    if(clicked):
        #create rectangle
        # (image, startpoint, end , color, thickness
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)
        # Create text
        text = getColorName(r,g,b) + "R = {} , G = {} , B = {}".format(r,g,b)
        #white text
        cv2.putText(img,text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        #for light colors use black
        if (r+g+b > 599):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)

        clicked=False

    if cv2.waitKey(20) and 0xFF == 27:
        # ESC KEY end this loop
        break

cv2.destroyAllWindows()
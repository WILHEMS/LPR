from cv2 import imread, imwrite, resize, cvtColor, COLOR_BGR2GRAY, threshold, THRESH_BINARY_INV, GaussianBlur
from os import listdir

in_dir = "/Users/shahargino/Downloads/IsraelLPR"
out_dir = "/Users/shahargino/Downloads/IsraelLPROut"

for img_file in listdir(in_dir):
    img = imread(in_dir+"/"+img_file)
    gray = cvtColor(img, COLOR_BGR2GRAY)
    blur = GaussianBlur(gray,(5,5),0)
    _, thresh = threshold(blur, 127, 255, THRESH_BINARY_INV)
    resized = resize(thresh, (20, 30))
    imwrite(out_dir+"/"+img_file, resized)

print "Done"

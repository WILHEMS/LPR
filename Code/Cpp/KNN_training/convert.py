# !/usr/bin/python
# (c) Shahar Gino, June-2017, sgino209@gmail.com

from sys import exit, argv
from getopt import getopt, GetoptError
from numpy import loadtxt, savetxt, float32, empty
from os import path, mkdir, chdir, system, listdir
from cv2 import imread, imwrite, cvtColor, COLOR_RGB2GRAY

__version__ = "1.0"

# Python structuring way:
class Struct:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

# ---------------------------------------------------------------------------------------------------------------
def main(_argv):
    """ Converts standard images to flattened images, and vice versus """

    # Default parameters:
    args = Struct(
        flattened_images="./flattened_images.txt",
        classifications="./classifications.txt",
        images_folder="./images",
        mode="pack",
        format="xml",
        flattened_size=(20,30),  # (width,height)
        debugMode=False
    )

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    # User-Arguments parameters (overrides Defaults):
    try:
        opts, user_args = getopt(_argv, "h", ["flattened_images=", "classifications=", "images_folder=",
                                              "mode=", "format=", "flattened_size=","debug"])

        for opt, user_arg in opts:
            if opt == '-h':
                usage()
                exit()
            elif opt in "--flattened_images":
                args.flattened_images = user_arg
            elif opt in "--classifications":
                args.classifications = user_arg
            elif opt in "--images_folder":
                args.images_folder = user_arg
            elif opt in "--mode":
                args.mode = user_arg
            elif opt in "--format":
                args.format = user_arg
            elif opt in "--flattened_size":
                args.flattened_size = user_arg
            elif opt in "--debug":
                args.debugMode = True

    except GetoptError:
        usage()
        exit(2)

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    # Convert:
    if args.mode == "unpack":
        unpack(args.flattened_images, args.classifications, args.images_folder, args.flattened_size, args.format)

    elif args.mode == "pack":
        pack(args.flattened_images, args.classifications, args.images_folder, args.flattened_size, args.format)

    else:
        usage()
        exit(2)

# ---------------------------------------------------------------------------------------------------------------
def pack(flattened_img, classifications, images_folder, flattened_size, fmt):
    """ Pack standard images into a flattened images + classifications pair format """

    N = flattened_size[0] * flattened_size[1]
    nImages = len([name for name in listdir(images_folder) if path.isfile(path.join(images_folder,name))])
    npaClassifications = empty((nImages,1))
    npaFlattenedImages = empty((nImages,N))
    k = 0
    for filename in listdir(images_folder):

        if filename == ".DS_Store":
            continue

        image = imread(path.join(images_folder, filename))
        image = cvtColor(image, COLOR_RGB2GRAY).reshape(1, N)
        if image is not None:
            npaFlattenedImages[k] = image
            npaClassifications[k] = ord(filename[0])
        k += 1

    if fmt == "txt":
        savetxt(classifications, npaClassifications, delimiter=' ', fmt='%1.18e')
        savetxt(flattened_img, npaFlattenedImages, delimiter=' ', fmt='%1.18e')

    elif fmt == "xml":
        with open(classifications, 'w') as classifications_file:
            classifications_file.write('<?xml version="1.0"?>\n')
            classifications_file.write('<opencv_storage>\n')
            classifications_file.write('<classifications type_id="opencv-matrix">\n')
            classifications_file.write('  <rows>'+str(nImages)+'</rows>\n')
            classifications_file.write('  <cols>1</cols>\n')
            classifications_file.write('  <dt>i</dt>\n')
            classifications_file.write('  <data>\n')
            i = 0
            for t in npaClassifications:
                if i % 24 == 0:
                    classifications_file.write("    %d " % t)
                elif i % 24 == 23:
                    classifications_file.write("%d " % t + '\n')
                elif i == nImages - 1:
                    classifications_file.write("%d" % t + '\n')
                else:
                    classifications_file.write("%d " % t)
                i += 1
            classifications_file.write('  </data>\n')
            classifications_file.write('</classifications>\n')
            classifications_file.write('</opencv_storage>\n')

            with open(flattened_img, 'w') as images_file:
                images_file.write('<?xml version="1.0"?>\n')
                images_file.write('<opencv_storage>\n')
                images_file.write('<images type_id="opencv-matrix">\n')
                images_file.write('  <rows>' + str(nImages) + '</rows>\n')
                images_file.write('  <cols>' + str(N) + '</cols>\n')
                images_file.write('  <dt>f</dt>\n')
                images_file.write('  <data>\n')
                i = 0
                for img in npaFlattenedImages:
                    for t in img:
                        if i % 14 == 0:
                            images_file.write("    %d. " % t)
                        elif i % 14 == 13:
                            images_file.write("%d. " % t + '\n')
                        elif i == nImages - 1:
                            images_file.write("%d." % t + '\n')
                        else:
                            images_file.write("%d. " % t)
                        i += 1
                images_file.write('  </data>\n')
                images_file.write('</images>\n')
                images_file.write('</opencv_storage>\n')

    else:
        print("ERROR: UnSupported format %s" % fmt)

# ---------------------------------------------------------------------------------------------------------------
def unpack(flattened_images, classifications, images_folder, flattened_size, fmt):
    """ Unpack flattened images and classifications pair into standard images format """

    if fmt == "xml":
        print("ERROR: UnSupported format %s" % format)
        return

    # Read in training classifications:
    try:
        npaClassifications = loadtxt(classifications, float32)
    except IOError:
        print("ERROR: Unable to open %s, exiting program" % classifications)
        system("pause")
        return

    # Read in training images:
    try:
        npaFlattenedImages = loadtxt(flattened_images, float32)
    except IOError:
        print("ERROR: Unable to open %s, exiting program" % flattened_images)
        system("pause")
        return

    # Create images folder:
    if not path.exists(images_folder):
        mkdir(images_folder, 0777)
    chdir(images_folder)

    # Convert:
    counters = {}
    for kClass in range(npaClassifications.size):
        className = npaClassifications[kClass]
        classNameStr = str(chr(int(className)))
        if className in counters:
            counters[className] += 1
        else:
            counters[className] = 0
        image = npaFlattenedImages[kClass].reshape(flattened_size[1],flattened_size[0])
        imwrite(classNameStr + "_" + str(counters[className]) + ".png", image)

# ---------------------------------------------------------------------------------------------------------------
def usage():
    """ Usage printout """

    script_name = path.basename(__file__)
    print 'Usage examples:'
    print '(1) %s --flattened_images=./flattened_images.txt --classifications=./classifications.txt --images_folder=./images --mode=pack' % script_name
    print '(2) %s --flattened_images=./flattened_images.txt --classifications=./classifications.txt --images_folder=./images --mode=unpack' % script_name
    print ''
    print 'Optional flags:  --flattened_size=(width,height) '
    print '                 --debug'
    print ''

# ---------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    main(argv[1:])
    print 'Done!'

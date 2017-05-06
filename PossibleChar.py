# !/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, May-2017, sgino209@gmail.com

from cv2 import boundingRect
from math import sqrt

# ---------------------------------------------------------------------------------------------------------------
class PossibleChar:
    """ Class for representing a contour which might be representing a possible character (for a later analysis) """

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    def __init__(self, _contour, MinPixelWidth, MaxPixelWidth, MinPixelHeight, MaxPixelHeight,
                 MinAspectRatio, MaxAspectRatio, MinPixelArea, MaxPixelArea):
        """ Constructor """

        self.contour = _contour

        self.boundingRect = boundingRect(self.contour)

        [intX, intY, intWidth, intHeight] = self.boundingRect

        self.intBoundingRectX = intX
        self.intBoundingRectY = intY
        self.intBoundingRectWidth = intWidth
        self.intBoundingRectHeight = intHeight

        self.intBoundingRectArea = self.intBoundingRectWidth * self.intBoundingRectHeight

        self.intCenterX = (self.intBoundingRectX + self.intBoundingRectX + self.intBoundingRectWidth) / 2
        self.intCenterY = (self.intBoundingRectY + self.intBoundingRectY + self.intBoundingRectHeight) / 2

        self.fltDiagonalSize = sqrt((self.intBoundingRectWidth ** 2) + (self.intBoundingRectHeight ** 2))

        self.fltAspectRatio = float(self.intBoundingRectWidth) / float(self.intBoundingRectHeight)

        self.MinPixelWidth = MinPixelWidth
        self.MaxPixelWidth = MaxPixelWidth
        self.MinPixelHeight = MinPixelHeight
        self.MaxPixelHeight = MaxPixelHeight
        self.MinAspectRatio = MinAspectRatio
        self.MaxAspectRatio = MaxAspectRatio
        self.MinPixelArea = MinPixelArea
        self.MaxPixelArea = MaxPixelArea

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    def checkIfPossibleChar(self):
        """ A 'first pass' over the contour, to see if it could be representing a character """

        return (self.MinPixelArea < self.intBoundingRectArea < self.MaxPixelArea and
                self.MinPixelWidth < self.intBoundingRectWidth < self.MaxPixelWidth and
                self.MinPixelHeight < self.intBoundingRectHeight < self.MaxPixelHeight and
                self.MinAspectRatio < self.fltAspectRatio < self.MaxAspectRatio)

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    def __sub__(self, other):
        """ Overloading the subtraction operator, with comparison that is based on centorid MSE metric (Pythagorean theorem) """

        return sqrt(((self.intCenterX - other.intCenterX) ** 2) +
                    ((self.intCenterY - other.intCenterY) ** 2))

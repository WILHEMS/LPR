# !/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, July-2017, sgino209@gmail.com

# ---------------------------------------------------------------------------------------------------------------
class PossiblePlate:
    """ Class for representing a (possible) license-plate object """

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    def __init__(self):
        """ Constructor """

        self.imgPlate = None
        self.imgGrayscale = None
        self.imgThresh = None
        self.rrLocationOfPlateInScene = None
        self.rrLocationOfPlateInSceneGbl = None
        self.strChars = ""
        self.rectFind = False

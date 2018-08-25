#!/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, July-2017, sgino209@gmail.com

import sys
import wx
from os import getcwd
from ast import literal_eval
from main import main as lpr_analyzer
from numpy import zeros, uint8, max, frombuffer
from cv2 import imread, resize, cvtColor, COLOR_RGB2BGR, rectangle, putText, FONT_HERSHEY_SIMPLEX

PANEL_SIZE = (1300,800)
IMAGE_SIZE = (600,600)
INF = 100000

debug = False

# ---------------------------------------------------------------------------------------------------------------
class lpr_gui_frame(wx.Frame):
    """ GUI class for LPR application """

    def __init__(self, parent):
        """ Frame Constructor """

        # -----------------------------------------------------------------------------------------------------
        # Frame initialization:

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="LPR GUI",
                          pos=wx.DefaultPosition, size=wx.Size(PANEL_SIZE[0], PANEL_SIZE[1]),
                          style=(wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL) & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        # -----------------------------------------------------------------------------------------------------
        # Main Sizer, Top side: Image Browser + Go button:

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.gSizer31 = wx.GridSizer(1, 2, 0, 0)

        self.m_filePicker1 = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*",
                                               wx.DefaultPosition, (600,-1), wx.FLP_DEFAULT_STYLE)
        self.m_filePicker1.SetToolTipString(u"Choose input image file\nType 'onvif' for capturing snaphot from IP camera")
        self.m_filePicker1.Bind(wx.EVT_FILEPICKER_CHANGED, self.OnSaveLogCheckBox)
        self.gSizer31.Add(self.m_filePicker1, 0, wx.ALL, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"Go!", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button2.Bind(wx.EVT_BUTTON, self.OnGoButton)
        self.gSizer31.Add(self.m_button2, 0, wx.ALL, 5)

        bSizer1.Add(self.gSizer31, 1, wx.EXPAND, 5)

        # -----------------------------------------------------------------------------------------------------
        # Main Sizer, Bottom side: Image viewer + User parameters:

        gSizer1 = wx.GridSizer(1, 2, 0, 0)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_bitmap1 = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        self.update_image(zeros((IMAGE_SIZE[0],IMAGE_SIZE[1], 3), uint8))
        bSizer2.Add(self.m_bitmap1, 0, wx.ALL, 5)

        m_textCtrl0 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (IMAGE_SIZE[0],100), wx.TE_MULTILINE|wx.VSCROLL)
        bSizer2.Add(m_textCtrl0, 0, wx.ALL, 5)
        sys.stdout = m_textCtrl0

        gSizer1.Add(bSizer2, 0, wx.ALL, 5)

        self.gSizer3 = wx.GridSizer(40, 2, 0, 0)

        self.m_textCtrl = []

        self.add_attribute("PreprocessGaussKernel", "(5,5)", "Preprocessing: gaussian kernel, for smoothing")
        self.add_attribute("PreprocessThreshBlockSize", "19", "Preprocessing: adaptive threshold, block size")
        self.add_attribute("PreprocessThreshweight", "9", "Preprocessing: adaptive threshold, weight")
        self.add_attribute("PreprocessMorphKernel", "(3,3)", "Preprocessing: morphological structuring kernel")
        self.add_attribute("PlateWidthPaddingFactor", "1.3", "Plate width padding factor, used for plate extraction")
        self.add_attribute("PlateHeightPaddingFactor", "1.5", "Plate height padding factor, used for plate extraction")
        self.add_attribute_combo("FindRectangledPlate", ["True","False"], "False", "Add another plate candidate, in addition to longest matching characters approach")
        self.add_attribute("ROI", "(-1,-1)", "ROI = (startX, startY, width, height)\n(0,0)=whole image, (-1,-1)=autoROI mode\nDiplayed image is 600x600")
        self.add_attribute("MinPixelWidth", "2", "Minimal width (#pixels) for a character to be detected")
        self.add_attribute("MaxPixelWidth", str(INF), "Maximal width (#pixels) for a character to be detected")
        self.add_attribute("MinPixelHeight", "8", "Minimal height (#pixels) for a character to be detected")
        self.add_attribute("MaxPixelHeight", str(INF), "Maximal height (#pixels) for a character to be detected")
        self.add_attribute("MinAspectRatio", "0.25", "Minimal aspect ratio (W/H) for a character to be detected")
        self.add_attribute("MaxAspectRatio", "1.0", "Maximal aspect ratio (W/H) for a character to be detected")
        self.add_attribute("MinPixelArea", "80", "Minimal area (#pixels) for a character to be detected")
        self.add_attribute("MaxPixelArea", str(INF), "Maximal area (#pixels) for a character to be detected")
        self.add_attribute("MinDiagSizeMultipleAway", "0.3", "Sizing factor for overlapping characters decision (% of character size)")
        self.add_attribute("MaxDiagSizeMultipleAway", "4", "Sizing factor for matching characters decision (% of character size)")
        self.add_attribute("MinChangeInArea", "0", "Normalized Area difference for matching characters decision, lower boundary")
        self.add_attribute("MaxChangeInArea", "0.5", "Normalized Area difference for matching characters decision, upper boundary")
        self.add_attribute("MinChangeInWidth", "0", "Normalized Width difference for matching characters decision, lower boundary")
        self.add_attribute("MaxChangeInWidth", "0.8", "Normalized Width difference for matching characters decision, upper boundary")
        self.add_attribute("MinChangeInHeight", "0", "Normalized Height difference for matching characters decision, lower boundary")
        self.add_attribute("MaxChangeInHeight", "0.2", "Normalized Height difference for matching characters decision, upper boundary")
        self.add_attribute("MinAngleBetweenChars", "0", "Angle difference (degrees) for matching characters decision, lower boundary")
        self.add_attribute("MaxAngleBetweenChars", "12.0", "Angle difference (degrees) for matching characters decision, upper boundary")
        self.add_attribute("MinNumberOfMatchingChars", "6", "Minimal amount of characters in the plate ('matching characters')")
        self.add_attribute("MaxNumberOfMatchingChars", "8", "Maximal amount of characters in the plate ('matching characters')")
        self.add_attribute("ResizedCharImageWidth", "20", "Character Resizing width attribute (in pixels), necessary for the OCR stage")
        self.add_attribute("ResizedCharImageHeight", "30", "Character Resizing height attribute (in pixels), necessary for the OCR stage")
        self.add_attribute_combo("NoVerticalAlign", ["True", "False"], "False", "Characters Vertical alignment, i.e. fix outlier characters along y-axis")
        self.add_attribute("kClassfications", getcwd()+"/KNN_training/classifications.txt", "KNN training data: classification results (see openCV docs)")
        self.add_attribute("kFlattenedImages", getcwd()+"/KNN_training/flattened_images.txt", "KNN training data: flattened images (see openCV docs)")
        self.add_attribute("kFactorKNN", "2", "KNN factor, for digits classification")
        self.add_attribute_combo("NoOcrTextualFixes", ["True", "False"], "False", "Do not perform manual OCR texutal corrections, e.g. 'I'-->'1'")
        self.add_attribute_combo("NoOcrKnnFixes", ["True", "False"], "False", "Do not perform manual OCR KNN corrections, e.g. '6'-->'5'")
        self.add_attribute_combo("NoOcrDigitsOnly", ["True", "False"], "False", "Do not drop OCR results with english alphabet characters (digits only)")
        self.add_attribute_combo("debugMode", ["True", "False"], "False", "Enable debug printouts and intermediate figures")
        self.add_attribute_combo("OpMode", ["auto", "default", "police"], "auto", "Run in a specific operational mode, e.g. 'police'")
        self.add_attribute_combo("batchMode", ["True", "False"], "True", "Run in batch mode, minimal debug info and w/o figures")

        self.m_textCtrl[7].Bind(wx.EVT_TEXT_ENTER, self.OnRoiText)

        gSizer1.Add(self.gSizer3, 1, wx.EXPAND, 5)

        bSizer1.Add(gSizer1, 1, wx.EXPAND, 5)

        # -----------------------------------------------------------------------------------------------------
        # Closure:
        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    # -----------------------------------------------------------------------------------------------------
    def OnSaveLogCheckBox(self, browseInfo):
        """ Image broswer handler, called when browser is updated """

        frame = imread(browseInfo.Path)
        if frame is None:
            self.update_image(zeros((IMAGE_SIZE[0], IMAGE_SIZE[1], 3), uint8))
        else:
            self.update_image(frame)

        if max(frame) > 0:
            self.draw_roi()

    # -----------------------------------------------------------------------------------------------------
    def OnGoButton(self, buttonInfo):
        """ Go button handler, called when Go button is clicked """

        in_frame = self.m_filePicker1.GetPath()
        if in_frame != "":
            cmd = ["-i", self.m_filePicker1.GetPath().encode("utf-8"),
                   "--PreprocessGaussKernel", self.m_textCtrl[0].GetValue().encode("utf-8"),
                   "--PreprocessThreshBlockSize", self.m_textCtrl[1].GetValue().encode("utf-8"),
                   "--PreprocessThreshweight", self.m_textCtrl[2].GetValue().encode("utf-8"),
                   "--PreprocessMorphKernel", self.m_textCtrl[3].GetValue().encode("utf-8"),
                   "--PlateWidthPaddingFactor", self.m_textCtrl[4].GetValue().encode("utf-8"),
                   "--PlateHeightPaddingFactor", self.m_textCtrl[5].GetValue().encode("utf-8"),
                   "--ROI", self.m_textCtrl[7].GetValue().encode("utf-8"),
                   "--MinPixelWidth", self.m_textCtrl[8].GetValue().encode("utf-8"),
                   "--MaxPixelWidth", self.m_textCtrl[9].GetValue().encode("utf-8"),
                   "--MinPixelHeight", self.m_textCtrl[10].GetValue().encode("utf-8"),
                   "--MaxPixelHeight", self.m_textCtrl[11].GetValue().encode("utf-8"),
                   "--MinAspectRatio", self.m_textCtrl[12].GetValue().encode("utf-8"),
                   "--MaxAspectRatio", self.m_textCtrl[13].GetValue().encode("utf-8"),
                   "--MinPixelArea", self.m_textCtrl[14].GetValue().encode("utf-8"),
                   "--MaxPixelArea", self.m_textCtrl[15].GetValue().encode("utf-8"),
                   "--MinDiagSizeMultipleAway", self.m_textCtrl[16].GetValue().encode("utf-8"),
                   "--MaxDiagSizeMultipleAway", self.m_textCtrl[17].GetValue().encode("utf-8"),
                   "--MinChangeInArea", self.m_textCtrl[18].GetValue().encode("utf-8"),
                   "--MaxChangeInArea", self.m_textCtrl[19].GetValue().encode("utf-8"),
                   "--MinChangeInWidth", self.m_textCtrl[20].GetValue().encode("utf-8"),
                   "--MaxChangeInWidth", self.m_textCtrl[21].GetValue().encode("utf-8"),
                   "--MinChangeInHeight", self.m_textCtrl[22].GetValue().encode("utf-8"),
                   "--MaxChangeInHeight", self.m_textCtrl[23].GetValue().encode("utf-8"),
                   "--MinAngleBetweenChars", self.m_textCtrl[24].GetValue().encode("utf-8"),
                   "--MaxAngleBetweenChars", self.m_textCtrl[25].GetValue().encode("utf-8"),
                   "--MinNumberOfMatchingChars", self.m_textCtrl[26].GetValue().encode("utf-8"),
                   "--MaxNumberOfMatchingChars", self.m_textCtrl[27].GetValue().encode("utf-8"),
                   "--ResizedCharImageWidth", self.m_textCtrl[28].GetValue().encode("utf-8"),
                   "--ResizedCharImageHeight", self.m_textCtrl[29].GetValue().encode("utf-8"),
                   "--kClassfications", self.m_textCtrl[31].GetValue().encode("utf-8"),
                   "--kFlattenedImages", self.m_textCtrl[32].GetValue().encode("utf-8"),
                   "--kFactorKNN", self.m_textCtrl[33].GetValue().encode("utf-8"),
                   "--mode", self.m_textCtrl[38].GetValue().encode("utf-8")]
                   
            if self.m_textCtrl[6].GetValue() == "True":
                cmd.append("--FindRectangledPlate")

            if self.m_textCtrl[30].GetValue() == "True":
                cmd.append("--NoVerticalAlign")

            if self.m_textCtrl[34].GetValue() == "True":
                cmd.append("--NoOcrTextualFixes")

            if self.m_textCtrl[35].GetValue() == "True":
                cmd.append("--NoOcrKnnFixes")

            if self.m_textCtrl[36].GetValue() == "True":
                cmd.append("--NoOcrDigitsOnly")

            if self.m_textCtrl[37].GetValue() == "True":
                cmd.append("--debug")

            if self.m_textCtrl[39].GetValue() == "True":
                cmd.append("--batch")

            if debug:
                print cmd

            out_frame = lpr_analyzer(cmd)
            if out_frame is not None:
                self.update_image(out_frame)

    # -----------------------------------------------------------------------------------------------------
    def OnRoiText(self, RoiInfo):
        """ ROI text control handler, called when text is updated """

        frame = imread(self.m_filePicker1.GetPath().encode("utf-8"))
        self.update_image(frame)
        self.draw_roi()

    # -----------------------------------------------------------------------------------------------------
    def update_image(self, in_frame):
        """ Auxiliary method for updating the image figure """

        frame_cvt = cvtColor(in_frame, COLOR_RGB2BGR)
        frameResized = resize(frame_cvt, (IMAGE_SIZE[0], IMAGE_SIZE[1]))
        w, h = frameResized.shape[:2]
        self.m_bitmap1.SetBitmap(wx.BitmapFromBuffer(w, h, frameResized))

    # -----------------------------------------------------------------------------------------------------
    def add_attribute(self, name, defval, tooltip):
        """ Auxiliary method for adding attribute parameter """

        m_staticText = wx.StaticText(self, wx.ID_ANY, name, wx.DefaultPosition, wx.DefaultSize, 0)
        m_staticText.Wrap(-1)
        m_staticText.SetToolTipString(tooltip)
        self.gSizer3.Add(m_staticText, 0, wx.ALL, 5)

        m_textCtrl = wx.TextCtrl(self, id=wx.ID_ANY, name=wx.EmptyString, pos=wx.DefaultPosition, size=(200,-1), style=wx.TE_PROCESS_ENTER)
        m_textCtrl.SetLabel(defval)
        m_textCtrl.SetToolTipString(tooltip)
        self.m_textCtrl.append(m_textCtrl)
        self.gSizer3.Add(m_textCtrl, 0, wx.ALL, 5)

    # -----------------------------------------------------------------------------------------------------
    def add_attribute_combo(self, name, combovals, defval, tooltip):
        """ Auxiliary method for adding attribute parameter """

        m_staticText = wx.StaticText(self, wx.ID_ANY, name, wx.DefaultPosition, wx.DefaultSize, 0)
        m_staticText.Wrap(-1)
        m_staticText.SetToolTipString(tooltip)
        self.gSizer3.Add(m_staticText, 0, wx.ALL, 5)

        m_comboBox = wx.ComboBox(self, wx.ID_ANY, defval, wx.DefaultPosition, (200,-1), combovals, 0)
        m_comboBox.SetToolTipString(tooltip)
        self.m_textCtrl.append(m_comboBox)
        self.gSizer3.Add(m_comboBox, 0, wx.ALL, 5)

    # -----------------------------------------------------------------------------------------------------
    def draw_roi(self):
        """ Auxiliary method for drawing ROI on the displayed image """

        bitmap = self.m_bitmap1.GetBitmap()
        image = wx.ImageFromBitmap(bitmap)
        buf = image.GetDataBuffer()
        frame = frombuffer(buf, dtype='uint8')
        frame = frame.reshape((IMAGE_SIZE[0],IMAGE_SIZE[1],3))

        imgH, imgW, _ = frame.shape

        roi = literal_eval(self.m_textCtrl[7].GetValue().encode("utf-8"))
        x1, y1, x2, y2 = 0, 0, 0, 0
        if len(roi) == 4:
            x1, y1, x2, y2 = roi[0], roi[1], roi[0] + roi[2], roi[1] + roi[3]
        elif roi[0] == 0:
            x1, y1, x2, y2 = 0, 0, imgW, imgH
        elif roi[0] == -1:
            x1, y1, x2, y2 = (int(0.2 * imgW), int(0.4 * imgH), int(0.8 * imgW), int(0.9* imgH))
        rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        putText(frame, "ROI", (x1+int(0.45*(x2-x1)), y1 - 10), FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        self.m_bitmap1.SetBitmap(wx.BitmapFromBuffer(IMAGE_SIZE[0], IMAGE_SIZE[1], frame))

    # -----------------------------------------------------------------------------------------------------
    def __del__(self):
        """ Destructor """
        pass

# ---------------------------------------------------------------------------------------------------------------
app = wx.App(False)
frame = lpr_gui_frame(None)
frame.Show()
app.MainLoop()
sys.stdout = sys.__stdout__

#!/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, July-2017, sgino209@gmail.com

import cv2
import urllib2
import numpy as np
from onvif import ONVIFCamera

class onvif_camera:

    # -----------------------------------------------------------------------------------------------------------
    def __init__(self, ip, port, user, passwd, wsdl='/Library/Python/2.7/site-packages/python-onvif-master/wsdl'):
        self.mycam = ONVIFCamera(ip, port, user, passwd, wsdl)

    # -----------------------------------------------------------------------------------------------------------
    def get_host_name(self):
        """ Get Hostname """

        resp = self.mycam.devicemgmt.GetHostname()
        cam_hostname = str(resp.Name)

        return cam_hostname

    # -----------------------------------------------------------------------------------------------------------
    def get_time_str(self):
        """ Get system date and time as a formatted string """

        dt = self.mycam.devicemgmt.GetSystemDateAndTime()
        day = dt.UTCDateTime.Date.Day
        month = dt.UTCDateTime.Date.Month
        year = dt.UTCDateTime.Date.Year
        hour = dt.UTCDateTime.Time.Hour
        minute = dt.UTCDateTime.Time.Minute
        second = dt.UTCDateTime.Time.Second

        frame_time = "%02d%02d%d_%02d%02d%02d" % (day, month, year, hour, minute, second)

        return frame_time

    # -----------------------------------------------------------------------------------------------------------
    def snaphot_capture(self):
        """ Capture a frame snapshot """

        media = self.mycam.create_media_service()

        allProfiles = media.GetProfiles()
        mainProfile = media.GetProfile({'ProfileToken' : allProfiles[0]._token})

        snapshot = media.GetSnapshotUri({'ProfileToken' : mainProfile._token})

        bin_array = urllib2.urlopen(snapshot.Uri).read()
        img_array = np.asarray(bytearray(bin_array), dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        return frame

# -----------------------------------------------------------------------------------------------------------
def onvif_snapshot_test():
    """ Simple ONVIF test: capture a snapshot and figure it """

    mycam = onvif_camera('192.168.226.201', 80, 'admin', '123456')

    frame = mycam.snaphot_capture()

    frame_title = mycam.get_host_name() + "_" + mycam.get_time_str()

    cv2.imshow(frame_title, frame)
    cv2.waitKey(0)

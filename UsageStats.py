#!/usr/bin/env python
"""

Parse usagestats from usagestats file - /data/system/usagestats/USER/daily
Events taken from from: https://developer.android.com/reference/android/app/usage/UsageEvents.Event.html (API 21+)

To view "on device" when application was last used:

adb shell am start -n com.android.settings/.UsageStatsActivity 

2019 @ https://github.com/Magpol

"""

from xml.dom import minidom
import os.path
import sys
import datetime

TIMEFORMAT="%Y-%m-%d %H:%M:%S"

EVENT_INDEXES = { 5: "CONFIGURATION_CHANGE - the device configuration has changed",
                18: "KEYGUARD_HIDDEN - user unlocks their phone after turning it on",
                17: "KEYGUARD_SHOWN - keyguard has been shown, whether or not the screen is off",
                2: "MOVE_TO_BACKGROUND - component moved to the background",
                1: "MOVE_TO_FOREGROUND - component moved to the foreground",
                15: "SCREEN_INTERACTIVE - turned on for full user interaction",
                16: "SCREEN_NON_INTERACTIVE - completely turned off or turned on only in a non-interactive state",
                7: "USER_INTERACTION - package was interacted with in some way by the user",
                0:"NONE"
                }

def main(args):
    if len(args) != 1:
        print("USAGE: parseUsagestats.py <FILE>")
        return -1

    filename = args[0]
    try:
        os.path.exists(filename)
    except FileNotFoundError:
        print("Error in filename")
    else:
        xmldoc = minidom.parse(filename)
        itemlistEvents = xmldoc.getElementsByTagName('event') 
        itemlistPackages = xmldoc.getElementsByTagName('package') 
        print("\n\n:: Package last activity ::")
        for s in itemlistPackages:
            timestring = datetime.datetime.fromtimestamp((int(filename)+int(s.attributes['lastTimeActive'].value))/1000).strftime(TIMEFORMAT)
            package = s.attributes['package'].value
            eventType = s.attributes['lastEvent'].value
            if int(eventType) in EVENT_INDEXES:
                eventType = EVENT_INDEXES[int(eventType)]    
            if eventType != "NONE":        
                print(timestring + " :: " + package + " :: " + eventType)

        print("\n\n:: Timeline ::")
        for s in itemlistEvents:
            timestring = datetime.datetime.fromtimestamp((int(filename)+int(s.attributes['time'].value))/1000).strftime(TIMEFORMAT)
            package = s.attributes['package'].value
            eventType = s.attributes['type'].value
            if int(eventType) in EVENT_INDEXES:
                eventType = EVENT_INDEXES[int(eventType)]            
            print(timestring + " :: " + package + " :: " + eventType)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

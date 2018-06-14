# import sys
import locale
import pandas
import re
import os
from os import walk, getcwd
from fnmatch import fnmatch

def getMessages(filePath):
    with open(filePath, encoding = "utf8") as myInputFile:
        user = ''
        for myLine in myInputFile:
            myLine = re.sub(',"(.*?)"', r';"\1"', myLine)
            myLine = re.sub(',', ';', myLine, count=1)
            message = myLine.split(';')
            if message[0].startswith("[Info]"):
                try:
                    if len(message) == 13:
                        user = message[7].strip('"')
                        messages.append(
                            ['t',                                               # Terminal to server message
                            message[0].replace('[Info] ', ''),                  # Date of server receieving message
                            message[1].strip('"'),                              # Time of server receieving message
                            message[6].strip('"'),                              # Terminal serial number
                            user,                                               # User
                            message[9].strip('"'),                              # Process name
                            message[8].strip('"'),                              # State
                            '' ,                                                # Terminal's prompt
                            message[12].replace('\n','').strip('"').strip()])   # Users's answer
                    else:
                        messages.append(
                            ['s',                                               # Server to terminal message
                            message[0].replace('[Info] ',''),                   # Date of server receieving message
                            message[1].strip('"'),                              # Time of server receieving message
                            message[4].strip('"'),                              # Terminal serial number
                            user,                                               # User
                            message[7].strip('"'),                              # Process name
                            message[3].strip('"'),                              # State
                            message[5].strip('"'),                              # Terminal's prompt
                            ''])                                                # Users's answer
                except:
                    # print('Processed file:\n'+ filePath)
                    # print('Processed line:\n' + myLine)
                    # print(sys.exc_info()[0])
                    print('.', end='', flush=True)
    print(flush=True)

fileDirectory = os.getcwd()
# fileDirectory = r'''C:\Projects\_NonTFS\Movianto\dist'''

messages = []
logFiles = []

for path, subdirs, files in os.walk(fileDirectory):
    for name in files:
        if fnmatch(name, "*.log"):
            logFiles.append(os.path.join(path, name))

for index, logFile in enumerate(logFiles):
    print("Processing %3d of %3d named %s" % (index + 1, len(logFiles), logFile), end='', flush=True)
    getMessages(logFile)

cols=['Types','Date','Time','Terminal','User','Process','State','Prompt','Answer']
df = pandas.DataFrame(messages, columns=cols)
# df = df.sort_values(by=['Date','Time'])

# df = df.loc[df['User'] == 'klet456mi']

print("Creating output file", flush=True)
df.to_csv(os.path.join(fileDirectory, "voice_log_report.csv"), sep=';', index=False, encoding=locale.getpreferredencoding())

print("Log report created and contains " + "{:,}".format(len(df)) + " records", flush=True)
#!/usr/bin/python

import atexit
import pyaudio
import wave
import audioop
import re
import urllib
import urllib2
import time, datetime
import ConfigParser
import pprint
import sys, os, inspect


from collections import deque 
from subprocess import *


cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"src")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

#import pywapi
#import forecastio
from googleSpeech import GoogleSpeech
from voiceConfig import VoiceConfig
from voiceWeather import VoiceWeather



p = pyaudio.PyAudio()

def runCommand( string ):
	cmd = vConfig.getConfig( string )
	if ( cmd is not None ):

            textString = ''
	    if ( cmd == "class:weather" ):
                VoiceWeather.speakWeather( vConfig, string )
	    else:	
	        p = Popen(cmd, shell=True, stdout=PIPE)
	        textString = p.communicate()[0].rstrip()

	return textString


def initStream():
    #open stream

    # List and find the correct input device
    print "========================== DETECTING AVAILABLE AUDIO DEVICES ========================="
    device_index = None
    device_max_rate = vConfig.RATE
    device_max_channels = vConfig.CHANNELS

    for i in range( p.get_device_count() ):
       devinfo = p.get_device_info_by_index(i)
       print( "Device %d: %s"%(i,devinfo["name"]) )
       if ( int( devinfo["maxInputChannels"] ) > 0 ):
	    print( "        * Input Device" )
	    device_index = i
            device_max_rate = int(devinfo["defaultSampleRate"])
            device_max_channels = int(devinfo["maxInputChannels"])

    print "======================================================================================"
    if ( vConfig.DEVICE == -1 ):
        print "Using Detected Input Device: " + str(device_index)
    else:
	device_index = int(vConfig.DEVICE)
	print "Using Configured Input Device: " + str(device_index)

    if ( device_max_rate < vConfig.RATE ):
        print "Setting Record Rate to Device max of: " + str(device_max_rate)
	vConfig.RATE = device_max_rate

    if ( device_max_channels < vConfig.CHANNELS ):
        print "Setting Record Channels to Device max of: " + str(device_max_channels)
	vConfig.CHANNELS = device_max_channels

    print "================================ DEVICE DETAILS ======================================"
    devinfo = p.get_device_info_by_index(device_index)
    pp = pprint.PrettyPrinter(indent=4)    
    pp.pprint( devinfo )
    print "======================================================================================"
   
	
    stream  = p.open(   format = pyaudio.paInt16,
                         channels = vConfig.CHANNELS,
                         rate = vConfig.RATE,
                         input = True,
                         input_device_index = device_index,
                         frames_per_buffer = vConfig.INPUT_FRAMES_PER_BLOCK)
    print stream
    return stream



def listen_for_speech():
    """
    Does speech recognition using Google's speech  recognition service.
    Records sound from microphone until silence is found and save it as WAV and then converts it to FLAC. Finally, the file is sent to Google and the result is returned.
    """


    stream = initStream()

    print "* listening. CTRL+C to finish."
    all_m = []
    data = ''
    #SILENCE_LIMIT = 2
    rel = vConfig.RATE/vConfig.INPUT_FRAMES_PER_BLOCK
    slid_win = deque(maxlen=vConfig.SILENCE_LIMIT*rel)
    started = False
    
    while (True):
        data = stream.read(vConfig.INPUT_FRAMES_PER_BLOCK)
        slid_win.append (abs(audioop.avg(data, 2)))

        if(True in [ x>vConfig.THRESHOLD for x in slid_win]):
            if(not started):
                print "starting record"
            started = True
            all_m.append(data)
        elif (started==True):
            print "finished"
            #the limit was reached, finish capture and deliver
            filename = save_speech(all_m,p)
	    print filename

            textString = GoogleSpeech.stt(filename, vConfig.RATE)
	    if ( textString != '' ):
		#os.system( "say " + str(textString) )
		print "Initiating Configuration Lookup"
		#cmd = vConfig.getConfig( textString )
		#if ( cmd is not None ):
		runCommand(textString)


            #reset all
            started = False
            slid_win = deque(maxlen=vConfig.SILENCE_LIMIT*rel)
            all_m= []
	    stream = initStream()
            print stream
            print "listening ... again"

    print "* done recording"
    stream.close()
    #p.terminate()


def save_speech(data, p):
    filename = 'output_'+str(int(time.time()))
    # write data to WAVE file
    data = ''.join(data)
    wf = wave.open(filename+'.wav', 'wb')
    wf.setnchannels(vConfig.CHANNELS)
    wf.setsampwidth(p.get_sample_size( pyaudio.paInt16 ))
    #wf.setframerate(RATE)
    wf.setframerate(16000)
    wf.writeframes(data)
    wf.close()
    return filename


def cleanup():
    print "Caught Exit.. Cleaning Up" 
    print "... Deleting any tmp audio files lying around"
    os.system( "rm output_*" )

#def speakWeather( string ):
        #location_code = vConfig.get( "weather", "weather_location_code" )
#
	#weather_com_result = pywapi.get_weather_from_weather_com( str(location_code ))
	#print weather_com_result
	#print string
#
#
	#lookupString = ''
	#### TODAY
	#if ( re.compile( "today", re.IGNORECASE ).findall( string ,1 )):
	    #todayData = weather_com_result['forecasts'][0]
	    #if ( todayData['day']['text'] != 'N/A' ):
		    #if ( int( todayData['day']['chance_precip'] ) > 40 ):
		        #lookupString = "Today will be " + str( todayData['day']['text'] ) + " with a chance of showers and a high of " + str( todayData['high'] ) + "degrees"
		    #else:
		        #lookupString = "Today will be " + str( todayData['day']['text'] ) + " with a high of " + str( todayData['high'] ) + "degrees"
            #else:
		    #if ( int(todayData['night']['chance_precip'] ) > 40 ):
		        #lookupString = "Tonight will be " + str( todayData['night']['text'] ) + " with a chance of showers"
		    #else:
		        #lookupString = "Tonight will be " + str( todayData['night']['text'] )
#
#
	### TONIGHT
	#elif ( re.compile( "tonight", re.IGNORECASE).findall( string ,1 )):
	    #todayData = weather_com_result['forecasts'][0]
	    #if ( int(todayData['night']['chance_precip'] ) > 40 ):
	        #lookupString = "Tonight will be " + str( todayData['night']['text'] ) + " with a chance of showers"
	    #else:
	        #lookupString = "Tonight will be " + str( todayData['night']['text'] )
#
	#### Tomorrow Night
	#elif ( re.compile( "tomorrow night", re.IGNORECASE).findall( string ,1 )):
	    #todayData = weather_com_result['forecasts'][1]
	    #if ( int(todayData['night']['chance_precip'] ) > 40 ):
	        #lookupString = "Tomorrow night will be " + str( todayData['night']['text'] ) + " with a chance of showers"
	    #else:
	        #lookupString = "Tomorrow night will be " + str( todayData['night']['text'] )

	#### TODAY
	#elif ( re.compile( "tomorrow", re.IGNORECASE ).findall( string ,1 )):
	    #todayData = weather_com_result['forecasts'][1]
	    #if ( todayData['day']['text'] != 'N/A' ):
		    #if (( int( todayData['day']['chance_precip'] ) > 40 ) or ( int( todayData['night']['chance_precip'] ) > 40 )):
		        #lookupString = "Tomorrow will be " + str( todayData['day']['text'] ) + " with a chance of showers and a high of " + str( todayData['high'] ) + " degrees"
		    #else:
		        #lookupString = "Tomorrow will be " + str( todayData['day']['text'] ) + " with a high of " + str( todayData['high'] ) + "degrees"
#
#
	#else:
	    #lookupString = "It is currently " + str(weather_com_result['current_conditions']['text']) + " and " + weather_com_result['current_conditions']['temperature'] + "degrees.\n\n" 
#
#
	#print lookupString
	### Work our magic
	#if ( lookupString != '' ):
	    #GoogleSpeech.tts( lookupString )
	#else: 
	    #GoogleSpeech.tts( "Sorry, Weather information un-available at this time, please try again later" )
        


	

if(__name__ == '__main__'):
    atexit.register(cleanup)


    #GoogleSpeech.tts("Hello, Welcome!")
    vConfig = VoiceConfig()
    listen_for_speech()
    



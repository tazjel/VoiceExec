VoiceExec
=========

Take Control of your PC with Voice Recognition via Google Speech to Text and Google Text to Speach.

This tool is based on the idea from Stephen Hickson ( http://stevenhickson.blogspot.ca/2013/06/voice-command-v30-for-raspberry-pi.html ).
VoiceCommand is a neat tool, however there were a couple issues with VoiceCommand that I wanted to resolve. The major one being I want to allow an indefinate amount of time for any given command.

This is in its early stages, so check back later on or feel free to jump in and lend a hand in writing a great Voice Exec front end for Home/PC Automation.
If you run into any issues.. Feel free to contact me: qpaulson@gmail.com


If you write any good add-on modules or find any good uses for this tool, feel free to email me the details!



Package Requirements
====================

You will need to install the following Python Libraries
 - pyaudio ( Device Control & Recording )
	https://pypi.python.org/pypi/PyAudio



Non Python Requrements
========================

 - flactools ( the flac command needs to be in your path )
 
 - mplayer ( the mplayer command needs to be in your path )

 - phue ( required if you intend to use the hue lights plugin ( class:hue\_lights ) in the configuration.
	This is available via pip as phue




Built In Modules
================

* Weather:  
	
	This is a built in weather module that searches the weather using the weather.com API.  It understands basic weather requests including:    
		- Weather Today? ( i.e. Whats the weather going to be like Today? )    
		- Weather Tonight? ( i.e. Whats the weather look like Tonight? )    
		- Weather Tomrrow? ( i.e. Hows the weather going to look Tomorrow? )       

	To make weather work, you need to set your location in the voiceExec configuration file.  
	You can find your code here: http://aspnetresources.com/tools/weatherIdResolver

	Its in its early stages, so it may say some interesting things. :) 



* Downloader:
	
	This is a built in BitTorrent initiator client for Transmission.  It takes your voice query and downlaods a matching torrent.

	To use this module you need to have:    
		- A Transmission torrent app/rpc server running somewhere that the module can connect to. ( the rpc server is enabled if you enabled the web UI )    
		- Your VoiceExec Downloader section configured correctly    

	Example: "Download Debian" -> This will download the latest debian ISO

	This tool currently uses ThePirateBay as its source of torrents.

* Hue\_Lights:

	This is a built in controller for Phillips Hue lights.  As noted above, it requires the phue module to be installed. It understands basic commands currently including:    
		- lights kitchen off - This would turn the lights either in a kitchen group or labeled as kitchen off    
		- lights kitchen on - This would turn the lights either in the kitchen group or labeled as kitchen on    
		- lights kitchen dim 100 - This would dim the light or group of lights labeled as kitchen by 100     
		- lights kitchen increase brightness by 100 - This would increase the brightness of the light or group of lights labeled as kitchen by 100     
		- lights kitchen set to maximum brightness - This would set the brightness of the light or group of lights from its current value to the max value of 254     
		- lights kitchen set to minimum - This would set the brightness of the light or group of lights from its current value to the minimum value of 0     

	Colors and schedules to come. :) 
		
	

Have Fun!

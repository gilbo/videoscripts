#!/usr/bin/env python

import sys
import os.path
import subprocess
import math

def run(cmd):
  return subprocess.check_output(cmd, shell=True)

INPUT_ERROR="""Needs 3 arguments!
  addbumper.py bumper.mp4 inputvideo.mp4 outputvide.mp4
"""
if len(sys.argv) != 4:
  raise Exception(INPUT_ERROR)

print 'Argument List:', str(sys.argv)

BUMPER_VID=sys.argv[1]
INPUT_VID =sys.argv[2]
OUTPUT_VID=sys.argv[3]

print "BUMPER_VID:  "+BUMPER_VID
print "INPUT_VID:   "+INPUT_VID
print "OUTPUT_VID:  "+OUTPUT_VID

if not os.path.isfile(BUMPER_VID):
  raise Exception("File "+BUMPER_VID+" was not found.")
if not os.path.isfile(INPUT_VID):
  raise Exception("File "+INPUT_VID+" was not found.")

PROBE_BUMPER_CMD = "ffprobe -v error -select_streams v:0 "+\
                   "-show_entries stream=height,width "+BUMPER_VID
PROBE_INPUT_CMD  = "ffprobe -v error -select_streams v:0 "+\
                   "-show_entries stream=height,width:stream=start_time "+\
                   INPUT_VID
# Probe frame dimensions from input files
bwin = int( run(PROBE_BUMPER_CMD + " | grep width  | sed s/width=//")  )
bhin = int( run(PROBE_BUMPER_CMD + " | grep height | sed s/height=//") )
iwin = int( run(PROBE_INPUT_CMD + "  | grep width  | sed s/width=//")  )
ihin = int( run(PROBE_INPUT_CMD + "  | grep height | sed s/height=//") )

istart = float( run(PROBE_INPUT_CMD +\
                "  | grep start_time | sed s/start_time=//") )

PROBE_INPUT_TIME_CMD = "ffprobe -v error -select_streams v:0 "+\
                       "-show_entries stream=start_time"+INPUT_VID

print "Bumper size: "+str(bwin)+" x "+str(bhin)
print "Input size:  "+str(iwin)+" x "+str(ihin)
print "Input start: "+str(istart)


baspect = float(bwin)/float(bhin)
iaspect = float(iwin)/float(ihin)

if baspect > iaspect: # then we'll crop horizontally (full height)
  rw    = bwin * ihin / bhin
  rh    = ihin
else: # we'll crop vertically (full width)
  rw    = iwin
  rh    = bhin * iwin / bwin


# try to use the non-re-encoding concat
if False:
  FILTER=\
  "[0:v:0] scale=w="+str(rw)+""":h=-1 [s];[s] setsar=sar=1/1 [scaled];
  [scaled] crop=w="""+str(iwin)+":h="+str(ihin)+""" [v];
    aevalsrc=0:duration=4 [a] """
  print "\n\n"+FILTER+"\n\n"

  run("ffmpeg -i "+BUMPER_VID+" -strict -2 "+\
  "-filter_complex \""+FILTER+"\""+\
  ' -map "[v]" -map "[a]" bumper_resized.mp4')

  # create list needed for concatenating files
  #run("""echo "# this is a comment
  #file 'bumper_resized.mp4'
  #file '"""+INPUT_VID+"""'
  #" >concatlist.txt""")

  # concatenate videos
  #run("ffmpeg -f concat -i concatlist.txt -c:a aac -c copy "+OUTPUT_VID)

# do concatenation with bumper conversion
if True:
  FILTER=\
  "[0:v:0] scale=w="+str(rw)+""":h=-1 [s];[s] setsar=sar=1/1 [scaled];
  [scaled] crop=w="""+str(iwin)+":h="+str(ihin)+""" [cropped];
    aevalsrc=0:duration=4 [asrc];
  [1:a:0] afade=t=in:d=1 [talkaudio];
  [cropped][asrc][1:v:0][talkaudio] concat=n=2:v=1:a=1 [v] [a]"""
  print "\n\n"+FILTER+"\n\n"

  #" -i "+INPUT_VID+
  #-aspect '+str(iwin)+":"+str(ihin)+\
  run("ffmpeg -i "+BUMPER_VID+\
  " -ss "+str(-istart)+" -i "+INPUT_VID+" -strict -2 "+\
  "-filter_complex \""+FILTER+"\""+\
  ' -map "[v]" -map "[a]" -c:a aac '+\
  " "+OUTPUT_VID)


#run("ffmpeg -i "+BUMPER_VID+" -strict -2 "+\
#"-filter_complex \""+CROP_FILTER+"\""+\
#' -aspect '+str(iwin)+":"+str(ihin)+\
#" bumper_resized.mp4")

#run("ffmpeg -i bumper_resized.mp4 -i "+INPUT_VID+" -strict -2"+\
#' -filter_complex'+\
#' "[0:v:0][0:a:0][1:v:0][1:a:0] concat=n=2:v=1:a=1 [v] [a]"'+\
#' -map "[v]" -map "[a]" '+OUTPUT_VID)

# create list needed for concatenating files
#run("""echo "# this is a comment
#file '"""+BUMPER_VID+"""'
#file '"""+INPUT_VID+"""'
#" >concatlist.txt""")

# concatenate videos
#run("ffmpeg -f concat -i concatlist.txt -c copy "+OUTPUT_VID)








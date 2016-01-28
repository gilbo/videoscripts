#!/usr/bin/env python

import sys
import os.path
import subprocess
import math

def run(cmd):
  return subprocess.check_output(cmd, shell=True)

def process_subdir(subdir):
  final_dir  = subdir+"/final/"
  bumper_dir = subdir+"/bumpered/"
  print( final_dir )
  for f in os.listdir(final_dir):
    if f.endswith(".mp4"): 
      print final_dir+f+"  ;  "+bumper_dir+f
      run('./addbumper.py bumper.mp4 "'+final_dir+f+'" "'+bumper_dir+f+'"')



process_subdir(os.getcwd()+"/left_room")
process_subdir(os.getcwd()+"/right_room")




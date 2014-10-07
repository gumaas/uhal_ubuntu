#!/usr/bin/python

# Python script to update the CACTUS RPM Pool
# 
# Author: Christos Lazaridis

import os, sys, fnmatch

def query_yes_no(question):
    valid = {"yes": True, "y": True, "no": False, "n": False}

    while True:
        choice = raw_input(question).lower()
        if choice in valid:
            return valid[choice]
        else:
            print "Please respond with 'yes/y' or 'no/n'.\n"

# expect exactly one argument, otherwise exit
if len(sys.argv) != 2 :
  print """Usage: """,sys.argv[0],""" [relnum]
Updates the RPM POOL from which the Puppet CACTUS snapshots are created.
The output POOL directory is /afs/cern.ch/user/c/cactus/www/release/POOL/slc6_x86_64

arguments:
   relnum  CACTUS release version number.
           Required to define the RPM source directory from the path:
           CACTUS_HOME/www/release/[relnum]>/slc6_x86_64/

"""
  sys.exit(0)
  
cactus_release = sys.argv[1]
cactus_package_list = [] # to keep track of packages already in the pool
unmatched_packages = []  # packages not found in the pool

source="/afs/cern.ch/user/c/cactus/www/release/"+cactus_release+"/slc6_x86_64"
dest="/afs/cern.ch/user/c/cactus/www/release/POOL/slc6_x86_64"

if not os.path.isdir(source) :
  print "ERROR: Source directory does not appear to exist!"
  print "Tried to read from",source
  exit(2)

print "Checking POOL contents..."
for root, dir, files in os.walk(dest):
  print root
  for items in fnmatch.filter(files, "*.rpm") :
    cactus_package_list.append(items)
  print ""  
  break
  
print "Looking for new packages..."
for root, dir, files in os.walk(source+"/base/RPMS"):
  print root
  for package in fnmatch.filter(files, "*.rpm") :
    if len(fnmatch.filter(cactus_package_list, package)) == 0 and "src.rpm" not in package :
      print "Package",package,"not found in pool"
      unmatched_packages.append(["../../"+cactus_release+"/slc6_x86_64/base/RPMS/",package])
  print ""  
  break

for root, dir, files in os.walk(source+"/updates/RPMS"):
  print root
  for package in fnmatch.filter(files, "*.rpm") :
    if len(fnmatch.filter(cactus_package_list, package)) == 0 and "src.rpm" not in package :
      print "Package",package,"not found in pool"
      unmatched_packages.append(["../../"+cactus_release+"/slc6_x86_64/updates/RPMS/",package])
  print ""  
  break

if len(unmatched_packages) > 0 :
  print "The following packages have been identified as new:"
  for package in unmatched_packages :
    print package[1]
    
  if query_yes_no("Continue? [y/N] ") :
    for package in unmatched_packages :
      print "Creating symlink for",package[1]
      os.chdir(dest)
      os.symlink(package[0]+package[1], package[1])
    sys.exit(0)
  else :
    print "No modifications made, exiting."
    sys.exit(0)
else :
  print "No new packages found, exiting."
  sys.exit(0)    
    
    
    

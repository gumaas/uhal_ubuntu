#!/bin/bash   

# Remove links 
find .. -maxdepth 1 -type l -exec rm -f {} \;

#!/bin/bash

sudo apt-get install libboost-all-dev
sudo apt-get install gcc-4.4
sudo apt-get install g++-4.4

bck_dir=`pwd`


cd /usr/bin

bck_gcc=`ls -l gcc | awk '{print $11}'`
bck_gpp=`ls -l g++ | awk '{print $11}'`

sudo ln -sf gcc-4.4 gcc
sudo ln -sf g++-4.4 g++ 

ls -l gcc*
ls -l g++*

echo "Make sure that gcc is linked to gcc-4.4 and g++ is linked to g++-4.4"
read -p "Press Enter to continue" 

cd "$bck_dir"

export CC=/usr/bin/gcc-4.4 CXX=/usr/bin/g++-4.4 C++=/usr/bin/g++-4.4 

make Set=uhal SHELL=/bin/bash

cd /usr/bin

sudo ln -sf $bck_gcc gcc
sudo ln -sf $bck_gpp g++

ls -l gcc*
ls -l g++*
echo "Make sure that gcc and g++ are linked to the latest compiler versions"

This directory contains some scripts that hopefully make developing the 
code easier.  Feel free to modify and improve.

Personally, I find it easier to often work with multiple versions of the 
repos.  The multiple versions arise because after major changes to the 
trunk I tend to checkout a fresh version and keep the old one as back up.  
I then change the sym links in my development area to point to the fresh 
version of the repos and rebuild the design.

The repository code (rep) is separate from the development area (dev).  

(1) Create a dev and rep dir.
(2) Create a dir in dev for a particular development (e.g. newsys)
(3) Copy the scripts file to dev/newsys/
(4) Set REPDIR in checkout.sh and run it.
(5) Set REPDIR in link.sh and run it.
(6) Set REPOS_BUILD_DIR in build.sh and run it.

Open ISE and start developing..






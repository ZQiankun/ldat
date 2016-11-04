#!/bin/bash
if [ $# -ne 1 ]; then
	echo "Arguments Error; Usage: $0 <password>"
	exit 1
fi 
password=$1

echo "$password" | sudo -S  rpm -ivh SDL_image-1.2.12-6.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh freerdp-libs-1.0.2-2.nk.1.i686.rpm 
echo "$password" | sudo -S  rpm -ivh ftgl-2.1.3-0.8.rc5.nk.1.i686.rpm 
echo "$password" | sudo -S  rpm -ivh game-music-emu-0.5.5-4.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh libGLEW-1.9.0-3.nk.1.i686.rpm 
echo "$password" | sudo -S  rpm -ivh libcddb-1.3.2-11.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh libchromaprint-0.7-2.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh libdvbpsi-1.2.0-1.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh libebml-1.3.0-1.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh libkate-0.3.8-7.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh libmad-0.15.1b-16.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh libmatroska-1.4.0-1.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh libprojectM-2.0.1-19.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh libtiger-0.3.4-5.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh libupnp-1.6.18-2.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh lzo-minilzo-2.06-4.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh libvncserver-0.9.9-7.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh live555-2014.10.21-1.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh minizip-1.2.7-10.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh twolame-libs-0.3.13-3.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh x265-libs-1.2-5.nk.2.i686.rpm
echo "$password" | sudo -S  rpm -ivh xcb-util-keysyms-0.3.9-2.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh zvbi-0.2.33-15.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh libmodplug-0.8.8.4-4.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh vlc-core-2.2.1-2.nk.1.i686.rpm
echo "$password" | sudo -S  rpm -ivh vlc-2.2.1-2.nk.1.i686.rpm
echo "vlc offline install completed." 	    


#!/bin/bash
if [ $# -ne 1 ]; then
	echo "Arguments Error; Usage: $0 <password>"
	exit 1
fi 
password=$1


echo "$password" | sudo -S dpkg -i libaacs0_0.3.0-4_i386.deb
echo "$password" | sudo -S dpkg -i libbluray1_1%3a0.2.1+git20111208.63e308d-3_i386.deb
echo "$password" | sudo -S dpkg -i libcddb2_1.3.2-3fakesync1_i386.deb
echo "$password" | sudo -S dpkg -i libcrystalhd3_1%3a0.0~git20110715.fdd2f19-4.1_i386.deb
echo "$password" | sudo -S dpkg -i libdvbpsi7_0.2.2-1_i386.deb
echo "$password" | sudo -S dpkg -i libdvdread4_4.2.0+20121016-1ubuntu1.1_i386.deb
echo "$password" | sudo -S dpkg -i libdvdnav4_4.2.0+20130225-1ubuntu0.1_i386.deb		
echo "$password" | sudo -S dpkg -i libebml3_1.2.2-2_i386.deb
echo "$password" | sudo -S dpkg -i libiso9660-8_0.83-1_i386.deb
echo "$password" | sudo -S dpkg -i libmatroska5_1.3.0-1_i386.deb
echo "$password" | sudo -S dpkg -i libresid-builder0c2a_2.1.1-12_i386.deb
echo "$password" | sudo -S dpkg -i libsdl-image1.2_1.2.12-3~exp1ubuntu2_i386.deb
echo "$password" | sudo -S dpkg -i libtiff4_3.9.7-0ubuntu1_i386.deb
echo "$password" | sudo -S dpkg -i libsdl-image1.2_1.2.10-3_i386.deb
echo "$password" | sudo -S dpkg -i libsidplay2_2.1.1-12_i386.deb
echo "$password" | sudo -S dpkg -i libtar0_1.2.11-8_i386.deb
echo "$password" | sudo -S dpkg -i libudev0_151-12_i386.deb
echo "$password" | sudo -S dpkg -r libupnp6
echo "$password" | sudo -S dpkg -i libupnp3_1%3a1.6.6-5.1ubuntu0.12.04.1_i386.deb
echo "$password" | sudo -S dpkg -i libva-x11-1_1.0.15-4_i386.deb
echo "$password" | sudo -S dpkg -i libvcdinfo0_0.7.23-4.1ubuntu1_i386.deb
echo "$password" | sudo -S dpkg -i vlc-data_2.0.8-0ubuntu0.12.04.1_all.deb
echo "$password" | sudo -S dpkg -i libvlccore5_2.0.8-0ubuntu0.12.04.1_i386.deb
echo "$password" | sudo -S dpkg -i libvlc5_2.0.8-0ubuntu0.12.04.1_i386.deb
echo "$password" | sudo -S dpkg -i libx264-120_0.120.2151+gita3f4407-2_i386.deb
echo "$password" | sudo -S dpkg -i libxcb-composite0_1.8.1-1ubuntu0.2_i386.deb
echo "$password" | sudo -S dpkg -i libxcb-keysyms1_0.3.8-1build1_i386.deb
echo "$password" | sudo -S dpkg -i libxcb-keysyms1_0.3.9-1_i386.deb
echo "$password" | sudo -S dpkg -i libxcb-randr0_1.8.1-1ubuntu0.2_i386.deb
echo "$password" | sudo -S dpkg -i libxcb-xv0_1.8.1-1ubuntu0.2_i386.deb
echo "$password" | sudo -S dpkg -i vlc-nox_2.0.8-0ubuntu0.12.04.1_i386.deb
echo "$password" | sudo -S dpkg -i vlc_2.0.8-0ubuntu0.12.04.1_i386.deb
echo "$password" | sudo -S dpkg -i vlc-plugin-notify_2.0.8-0ubuntu0.12.04.1_i386.deb
echo "$password" | sudo -S dpkg -i vlc-plugin-pulse_2.0.8-0ubuntu0.12.04.1_i386.deb

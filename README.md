LbpLibrary
==========

Required Dependencies
---------------------
* C/C++ Compiler 
* Cmake
* Python 2/3 ( NumPy, ctypes )

Installation Guide on ubutnu 18.04 with Python 3.x
-------------------------------
1. In home direcotry, clone the project

	kai@kai-VirtualBox:~$ git clone https://github.com/neduchal/lbpLibrary.git

This will create a lbpLibrary folder containing all the github project files.

2. Create a folder where you like to compile the library

	kai@kai-VirtualBox:~/projects$ mkdir lbpLibrary
	
Jump in to this folder

	kai@kai-VirtualBox:~/projects$ cd lbpLibrary
	
3. Compile the library for python3

	kai@kai-VirtualBox:~/projects/lbpLibrary$ cmake ../../lbpLibrary
	kai@kai-VirtualBox:~/projects/lbpLibrary$ sudo make install
	kai@kai-VirtualBox:~/projects/lbpLibrary$ sudo python3 setup.py install

4. Now, the library is installed in system. You can test it

	kai@kai-VirtualBox:~/projects/lbpLibrary$ python3

	Python 3.6.7 (default, Oct 22 2018, 11:32:17) 
	[GCC 8.2.0] on linux
	Type "help", "copyright", "credits" or "license" for more information.
	>>> from lbp import *
	>>> lbp3d
	<module 'lbp.lbp3d' from '/usr/local/lib/python3.6/dist-packages/lbp/lbp3d.py'>

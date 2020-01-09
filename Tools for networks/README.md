
➢ Intro
While working as a TAC, I’ve experienced those below continuously. This is to help others who are not good at operating Juniper router product, or troubleshooting.
	1) How to collect system outputs continuously without using shell script.
	2) What/how to collect syslog log messages at a production, when problem occurred.
	3) How to simulate packets to troubleshoot
	4) ……various reasons

➢ Building Environment.
	- Based on Juniper Router products.(MX/T/PTX series) Other vendor’s would not work properly.
	- Building environment : You have to have installed python 3.7.2, pyqt5, and scapy module
		1) Install python 3.7.2 or higher version. Then set PATH env properly.
		2) In the directory, install pyqt5 and scapy module
			Move into the directory where all files are exist.
			#cd C:\Python37\studyrootm\project\Tools for networks_V2
	- Released 3 files
		1) “Tools for networkers.py” :
		2) “Window_ui.zip” : GUI application designed with PYQT5
		3) ”Release_note_v2.1”
	- How to Run
		To run it, you need 2 files exist in the same dir “Tools for Networkers and Window.ui”.
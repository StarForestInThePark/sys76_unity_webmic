Web/Microphone muting application
-------------------

This application was created as I was annoyed that there was not a Unity app 
that I could use to quickly check my webcam and microphone status.

It assumes a couple things:
 * Gtk2 and its python bindings are installed and available.
 * the requirements.txt file is installed
 * this uses the amixer command so if its not available for your system, too bad.
 * It assumes that you have a uvcvideo USB webcam.

Before this will work you will need to add the following line to your sudoers file:

Example:
    raptorx  ALL=NOPASSWD: /sbin/modprobe uvcvideo

If you want this to load on login add an entry using Ubuntu's StartupApplications.

If you have an application that is currently using the video driver it will not
work until the application is closed.


This was originally created and tested on and for a Gazelle System76 laptop.


Issues: 
    
    
    Hardcoded icon path, need to create a make install or use a gtk theme.

TODO: 
    
    
    Create and use GTK theme to remove the icons hardcoded path and create icons 
    to give visual feedback of the microphones/webcams status.

    
    Package this and create an installer for unity application indicator.

# -*- coding: utf-8 -*-

import gtk
import appindicator
import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop

import webmic


mic_status_message = "{status} Microphone"
webcam_status_message = "{status} WebCam"
en_den = lambda x: "Enable" if x else "Disable"

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

label_change = lambda window, message, t_status: window.set_label(
    message.format(status=en_den(t_status)))

def dbus_mic_status_listener(*args, **kwargs):
    ''' This receives the status updates from the microphone if muted/unmuted
    externally to keep the state consistent '''

    mute_state = args[0][0][1]['x-canonical-ido-voip-input-mute'] # ugly
    label_change(mic_label, mic_status_message, mute_state)

def menu_click(window, buf):
    if buf == 'web':
        webmic.webcam_toggle()
        label_change(window, webcam_status_message, webmic.webcam())
    elif buf == 'mic':
        webmic.microphone_toggle()
        label_change(window, mic_status_message, webmic.microphone())

if __name__ == '__main__':
    global mic_label
    global wc_label

    indicator = appindicator.Indicator('webcam-status-indicator',
                                       # TODO: create icons and use themes man
                                       '/home/matt/work/unity/icon.png', # icon definition
                                       appindicator.CATEGORY_HARDWARE)
    indicator.set_status(appindicator.STATUS_ACTIVE)

    menu = gtk.Menu()

    mic_label = gtk.MenuItem(
        mic_status_message.format(
            status=en_den(webmic.microphone())
        )
    )

    wc_label = gtk.MenuItem(
        webcam_status_message.format(
            status=en_den(webmic.webcam())
        )
    )

    wc_label.connect('activate', menu_click, "web")
    mic_label.connect('activate', menu_click, "mic")

    menu.append(mic_label)
    menu.append(wc_label)

    mic_label.show()
    wc_label.show()
    indicator.set_menu(menu)
    bus.add_signal_receiver(dbus_mic_status_listener,
                            dbus_interface="com.canonical.dbusmenu",
                            path="/com/canonical/indicator/sound/menu",
                            )

    loop = gobject.MainLoop()
    loop.run()
    gtk.main()

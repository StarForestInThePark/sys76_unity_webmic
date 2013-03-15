# -*- coding: utf-8 -*-

import gtk
import appindicator
import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop

import webmic

MIC_ICON_PATH = '/home/matt/work/unity/icons/{0}'
WC_ICON_PATH = '/home/matt/work/unity/icons/{0}'

MIC_ENABLED = MIC_ICON_PATH.format('mic_red.png')
MIC_DISABLED = MIC_ICON_PATH.format('mic_green.png')
MIC_ICON = MIC_ICON_PATH.format('mic.png')

EYE_ENABLED = WC_ICON_PATH.format('eye_green.png')
EYE_DISABLED = WC_ICON_PATH.format('eye_red.png')
EYE_ICON = WC_ICON_PATH.format('eye.png')

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
    set_mic_icon()

def menu_click(window, buf):
    if buf == 'web':
        webmic.webcam_toggle()
        label_change(window, webcam_status_message, webmic.webcam())
        set_wc_icon()
    elif buf == 'mic':
        webmic.microphone_toggle()
        label_change(window, mic_status_message, webmic.microphone())
        set_mic_icon()

def set_wc_icon():
        if webmic.webcam():
            wc_indicator.set_icon(EYE_DISABLED)
        else:
            wc_indicator.set_icon(EYE_ENABLED)

def set_mic_icon():
        if webmic.microphone():
            indicator.set_icon(MIC_ENABLED)
        else:
            indicator.set_icon(MIC_DISABLED)


if __name__ == '__main__':
    global mic_label
    global wc_label
    global indicator

    indicator = appindicator.Indicator('microphone-status-indicator',
                                       # TODO: create icons and use themes man
                                       MIC_ICON,
                                       appindicator.CATEGORY_HARDWARE)
    indicator.set_status(appindicator.STATUS_ACTIVE)

    wc_indicator = appindicator.Indicator('webcam-status-indicator',
                                       # TODO: create icons and use themes man
                                       EYE_ICON,
                                       appindicator.CATEGORY_HARDWARE)
    wc_indicator.set_status(appindicator.STATUS_ACTIVE)


    menu = gtk.Menu()
    wc_menu = gtk.Menu()

    mic_label = gtk.MenuItem(
        mic_status_message.format(
            status=en_den(webmic.microphone())
        )
    )
    set_mic_icon()

    wc_label = gtk.MenuItem(
        webcam_status_message.format(
            status=en_den(webmic.webcam())
        )
    )
    set_wc_icon()

    wc_label.connect('activate', menu_click, "web")
    mic_label.connect('activate', menu_click, "mic")

    menu.append(mic_label)
    wc_menu.append(wc_label)

    mic_label.show()
    wc_label.show()

    indicator.set_menu(menu)
    wc_indicator.set_menu(wc_menu)

    bus.add_signal_receiver(dbus_mic_status_listener,
                            dbus_interface="com.canonical.dbusmenu",
                            path="/com/canonical/indicator/sound/menu",
                            )

    loop = gobject.MainLoop()
    loop.run()
    gtk.main()

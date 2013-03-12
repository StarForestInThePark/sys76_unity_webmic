# -*- coding: utf-8 -*-

import gtk
import appindicator

import webmic


def menu_click(window, buf):
    if buf == 'web':
        webmic.webcam_toggle()
        window.set_label(
            webcam_status_message.format(
                status=en_den(webmic.webcam())
            )
        )
    elif buf == 'mic':
        webmic.microphone_toggle()
        window.set_label(
            mic_status_message.format(
                status=en_den(webmic.microphone())
            )
        )

mic_status_message = "{status} Microphone"
webcam_status_message = "{status} WebCam"
en_den = lambda x: "Enable" if x else "Disable"

if __name__ == '__main__':
    indicator = appindicator.Indicator('webcam-status-indicator',
                                       'indicator-messages', # icon definition
                                       appindicator.CATEGORY_HARDWARE)
    indicator.set_status(appindicator.STATUS_ACTIVE)
    indicator.set_attention_icon('indicator-messages-new')

    menu = gtk.Menu()

    mic_menu_item = gtk.MenuItem(
        mic_status_message.format(
            status=en_den(webmic.microphone())
        )
    )

    webcam_menu_item = gtk.MenuItem(
        webcam_status_message.format(
            status=en_den(webmic.webcam())
        )
    )
    webcam_menu_item.connect('activate', menu_click, "web")
    mic_menu_item.connect('activate', menu_click, "mic")

    menu.append(mic_menu_item)
    menu.append(webcam_menu_item)

    mic_menu_item.show()
    webcam_menu_item.show()
    indicator.set_menu(menu)

    gtk.main()



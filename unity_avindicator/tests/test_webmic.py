# -*- coding: utf-8 -*-

from unittest import TestCase

from unity_avindicator.webmic import main
from unity_avindicator import webmic

class TestWebmic(TestCase):
    def test_command_line(self):
        main()
    def test_microhone_toggle(self):
        prev_status = webmic.microphone()

        webmic.microphone_toggle()

        assert prev_status != webmic.microphone(), \
                "Toggling the microphones mute capability failed"

        # retore to its original state
        webmic.microphone_toggle()

    def test_webcam_toggle(self):
        prev_status = webmic.webcam()

        webmic.webcam_toggle()

        assert prev_status != webmic.webcam(), \
                "Toggling the webcams status has failed"

        #retore to previous state
        webmic.webcam_toggle()


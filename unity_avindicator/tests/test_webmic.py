# -*- coding: utf-8 -*-

from unittest import TestCase

import webmic
from unity_avindicator.webmic import main


class TestWebmic(TestCase):
    def test_command_line(self):
        main()


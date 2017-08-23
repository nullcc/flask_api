#!/usr/bin/env python
# -*- coding: utf-8 -*-

from blinker import Namespace

signals = Namespace()
model_saved = signals.signal('model_saved')

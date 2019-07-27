#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pysesame2 import get_sesames
import time

class SesameClient(object):
    _sesames = None

    def __init__(self, apikey=None):
        self._sesames = get_sesames(apikey)

    def unlock_all(self):
        tasks = list()
        for s in self._sesames:
            tasks.append(s.async_unlock())
        task_count = len(self._sesames)
        succeeded = 0
        while task_count != succeeded:
            succeeded = 0
            for s in tasks:
                if s.pooling():
                    succeeded +=1
            time.sleep(1)
        return True
    
    def get_status(self):
        for s in self._sesames:
            print(s.get_status())
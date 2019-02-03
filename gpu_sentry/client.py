# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2019 Grzegorz Jacenków
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Client-side application logic, i.e. monitoring GPU instances."""

import socket

from pynvml import (
    NVMLError,
    nvmlDeviceGetCount,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetName,
    nvmlInit,
)

from twisted.internet import task, reactor
import requests

from gpu_sentry import config


def _convert_kb_to_gb(size):
    """Convert given size in kB to GB with 2-decimal places rounding."""
    return round(size / 1024 ** 3, 2)


def get_statistics():
    """Get statistics for each GPU installed in the system."""
    nvmlInit()
    statistics = []

    try:
        count = nvmlDeviceGetCount()
        for i in range(count):
            handle = nvmlDeviceGetHandleByIndex(i)

            memory = nvmlDeviceGetMemoryInfo(handle)

            statistics.append({
                "gpu": i,
                "name": nvmlDeviceGetName(handle).decode("utf-8"),
                "memory": {
                    "total": _convert_kb_to_gb(int(memory.total)),
                    "used": _convert_kb_to_gb(int(memory.used)),
                    "utilisation": int(memory.used / memory.total * 100)
                },
            })
    except NVMLError as error:
        print(error)

    return statistics


def send_statistics():
    """Send statistics to the server-side API."""
    host = socket.gethostname()

    requests.post(config.SERVER_HOSTNAME,
                  json={"codename": config.PERMIT_CLIENTS[host]['codename'],
                        "name": config.PERMIT_CLIENTS[host]['name'],
                        "hostname": host,
                        "statistics": get_statistics()})


def run_client():
    """Run client to send statistics periodically."""
    l = task.LoopingCall(send_statistics)
    l.start(config.CLIENT_TIMEOUT)

    reactor.run()

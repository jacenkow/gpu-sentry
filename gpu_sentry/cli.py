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

"""Command-line interface (CLI)."""

import argparse

from gpu_sentry.client import run_client
from gpu_sentry.server import run_server


def cli():
    """Main method to run client- or server-side monitor."""
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--mode", required=True, type=str,
                    help="Select client- or server-side mode.")

    args = vars(ap.parse_args())

    if args['mode'] == "client":
        run_client()
    elif args['mode'] == "server":
        run_server()
    else:
        raise ValueError("Invalid mode selected. Select `client` or `server`.")


if __name__ == "__main__":
    cli()

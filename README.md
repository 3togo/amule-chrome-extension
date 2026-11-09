# aMule Chrome extension

A Chrome extension that opens eD2k links from web pages in aMule.

Chromium blocks `ed2k://` links that contain a literal `|`. The extension encodes each `|` as `%7C` before the click goes through. aMule 3.1.0 or later accepts the encoded form.

The extension is not released yet.

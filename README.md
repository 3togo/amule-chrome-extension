# eD2k Link Fixer

A Manifest V3 Chrome extension that makes eD2k links on web pages open in the
computer's registered eD2k application. Chromium rejects links containing literal
`|` characters; the extension replaces those characters with `%7C` before normal
link activation. Existing filename escapes and other URL schemes are preserved.

Install **aMule 3.1.0 or later** and enable its eD2k link-handler registration
in **Preferences → General**. Version 3.1.0 is the first aMule release that
accepts `%7C` delimiters and provides handler registration. Another application
must support encoded delimiters and be registered for `ed2k:` to work.
This extension does not install or register aMule. It needs no native messaging
host, background service or download-directory watcher.

## Install

1. Download `ed2k-link-fixer.zip` from the assets of a
   [GitHub release](https://github.com/amule-org/amule-chrome-extension/releases)
   and extract it. If no release is available yet, use a source checkout.
2. Open `chrome://extensions`, enable **Developer mode**, select **Load unpacked**
   and choose the directory containing `manifest.json`.
3. Refresh web pages that were open before installation.
4. Click an eD2k link and allow Chrome to open your application when prompted.

Keep the extracted folder in a permanent location. Remove or reload the extension
on Chrome's Extensions page. This is a local installation, not a Chrome Web Store
listing. See [Chrome's installation guide](https://developer.chrome.com/docs/extensions/get-started/tutorial/hello-world).
The toolbar button opens help and privacy information.

## Scope and privacy

Links on HTTP/HTTPS pages, matching frames and links added or changed after page
load are repaired. Normal clicks, keyboard activation and middle clicks keep the
browser's normal behavior. Open shadow-root links are also repaired on activation, including href changes
made by page click handlers. Activation support survives `document.open()` and
links moving between open shadow roots.
The extension does not synthesize navigation or bypass browser permission prompts.

Restricted browser pages and local files are outside its scope. Plain-text URLs,
closed shadow roots and controls that construct their own URLs in JavaScript may
need to be copied into aMule. Bulk queuing is not provided.

A canonical file link whose filename contains `%7C` or `%7c` is left unchanged.
Encoding its separators would make those filename escapes indistinguishable from
separators at the receiving application. Copy that original link into aMule;
preserving it avoids rejection or interpreting filename text as transfer metadata.

Site access is required to find links across websites. All processing happens in
the browser: no analytics, storage, external requests or native helper. Site access
can be restricted in Chrome's extension details.

A minimal Linux session with an older generic `xdg-open` can report that the
eD2k URL is a missing file even when the handler is registered. Update those
desktop utilities or use a working desktop/GIO integration for the handler.

Linux is the validated OS. Windows and macOS require their own working OS handler
and have not been tested. Other Chromium-based browsers have not been validated
with this packaged version.

## Development

Build instructions, test prerequisites and harness coverage are in
[DEVELOPING.md](https://github.com/amule-org/amule-chrome-extension/blob/master/DEVELOPING.md). Release and platform checks are in
[RELEASING.md](https://github.com/amule-org/amule-chrome-extension/blob/master/RELEASING.md).

## License

GPL-2.0-or-later, like aMule. See [LICENSE.txt](LICENSE.txt).

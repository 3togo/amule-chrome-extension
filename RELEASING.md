# First-release checks

Linux has automated logging-handler coverage. The optional Linux application
smoke test verifies the aMule queue. Windows and macOS handoff have **not** been
validated. A release workflow alone does not establish platform support.

## Windows and macOS handoff

Run these checks on each OS using the intended release ZIP and aMule **3.1.0 or
later**, with a private test profile/configuration. Record OS, Chrome and aMule
versions, the extension tag/commit, registration method and actual queue results.
Use aMule's own handler registration in Preferences → General; a substituted
logging handler does not establish that its Windows/macOS registration works.

1. Enable aMule's handler registration. On Windows, confirm the OS associates
   `ed2k:` with that aMule installation. On macOS, confirm the registered aMule
   app is the one launched, including when it was initially closed.
2. Extract the ZIP and load its `ed2k-link-fixer` folder using **Load unpacked**
   in `chrome://extensions`. Serve the following fixture over HTTP, for example
   with `python3 -m http.server 8000` in the folder containing it:

   ```html
   <!doctype html><meta charset="utf-8">
   <a href="ed2k://|file|release%20check.bin|123|0123456789abcdef0123456789abcdef|/">Queue test</a>
   <a href="ed2k://|file|literal%257Cname.bin|124|1123456789abcdef0123456789abcdef|/">Escaped percent test</a>
   <a href="ed2k://|file|cancelled.bin|125|2123456789abcdef0123456789abcdef|/">Cancel test</a>
   ```

3. Open the fixture in Chrome and inspect the first link: separators should be
   `%7C`, while its filename still contains `%20`. Click it and accept Chrome's
   external-application prompt. Verify aMule's queue contains `release check.bin`,
   size 123, hash `0123456789abcdef0123456789abcdef`.
4. Click the second link and verify the queue contains `literal%7Cname.bin`,
   size 124, hash `1123456789abcdef0123456789abcdef`. Filename text must not
   become a delimiter or be decoded twice.
5. Click the third link and cancel Chrome's prompt. Confirm that no transfer
   with its hash was added. Click again, accept, and confirm the matching name,
   size and hash appear. If Chrome remembered permission, reset that permission
   before the cancellation check.
6. Repeat with aMule already running and initially closed, removing the test
   transfers between runs so duplicate detection cannot mask a failed handoff.
   Remove the test transfers afterwards. Do not rely on a launch message alone.

Keep the browser's real permission prompt enabled. These synthetic hashes are
for queue inspection only; successful peer transfer is outside this check.

## Release ZIP

Follow the tag procedure in [DEVELOPING.md](DEVELOPING.md) after reviewing the
platform evidence and any remaining limitations. The upstream tag workflow
publishes a GitHub release asset built from that tag, rather than requiring users
to retrieve a CI artifact. Download and extract the attached ZIP, load its
`ed2k-link-fixer` directory in Chrome, and check the toolbar help and a link click.
A first release remains pending until a maintainer pushes an approved version tag
and the release asset is verified.

## Chrome Web Store

There is no store listing or agreed publisher account. Maintainers must designate
an account owner before store submission; no personal account is assumed by the
release workflow. Store publication is not performed by this repository's CI.

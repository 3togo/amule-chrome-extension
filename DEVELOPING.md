# Development and releases

## Build and test

Requires Node.js 22 or newer and Python 3. Run from this directory:

```sh
npm ci
npx playwright-core install chromium
npm test
npm run package
```

The ZIP is written to `dist/ed2k-link-fixer.zip`. The package script includes only
runtime assets, help, README and GPL license; no browser profiles or test output.
No build step is needed to load the source directory as an unpacked extension.

Set `AMULE_BROWSER_EXECUTABLE` to test an existing compatible Chromium executable
instead of Playwright's browser, for example `/usr/bin/google-chrome` on Linux.
The browser must support CDP's unpacked-extension loading for the smoke test.

On Debian/Ubuntu, install the Linux smoke-test prerequisites:

```sh
sudo apt-get install xvfb xauth dbus-x11 desktop-file-utils python3-gi gir1.2-atspi-2.0 at-spi2-core libxtst6 xdg-utils libglib2.0-bin
npm run test:smoke
```

The smoke test builds and extracts the ZIP, runs a headed browser under a private
X server and D-Bus session, and registers a logging handler in private XDG
folders. It checks the blocked control, native first-use permission prompt,
handler delivery, dynamic links, frames, site cancellation and recovery, page
click handlers, filename escapes, activation methods and bundled help.
The default smoke test establishes OS handoff; it does not require aMule.
CI declares a GNOME/GIO desktop route. Older generic `xdg-open` releases
misclassify digit-containing schemes such as `ed2k:` as file paths; the
[legacy scheme check](https://sources.debian.org/src/xdg-utils/1.1.3-4.1/scripts/xdg-open.in/)
shows that limitation. A modern generic launcher can also run the smoke test.
The optional application test also queries the actual EC queue and compares exact
filenames, file hashes and sizes, including the absence of cancelled transfers.

To additionally verify actual download-queue acceptance in an isolated aMule:

```sh
AMULE_SOURCE_DIR=/path/to/amule-source \
AMULE_BINARY=/path/to/current/amule-or-amuled npm run test:smoke
```

The optional application test also requires Python cryptography
(`sudo apt-get install python3-cryptography`). Use a current source build
compatible with the documented eD2k command line and maintained EC test peer.
`AMULE_SOURCE_DIR` must point to its matching aMule source checkout; the fixture
imports `unittests/tests/DaemonConfig.py` and `AllSearchIntegrationTest.py` from
that checkout. The extension repository does not vendor these aMule helpers.
Missing or unusable source helpers, including the EC authentication dependencies,
return exit code 77 during preflight. Relative source and binary paths (including
paths with spaces and binaries found on `PATH`) are resolved before desktop launch.
Older installed versions can fail escaped-filename checks because of their own
decoding behavior; do not weaken those assertions to accept a changed filename. Autoconnection, Kad and UPnP are disabled in its private config.
The fixture seeds `lastversion` for GIT, 3.0.1 and 3.2.0 to avoid the first-run
version notice. Add the tested version there when testing another release.
Smoke tests retain their evidence in the printed temporary directory. Missing
prerequisites return exit code 77 before fixture processes start.

The repository CI runs the DOM unit tests, application preflight regressions
against pinned aMule source helpers, and the Linux logging-handler smoke test.
To run the preflight regressions locally with the dependencies listed above:

```sh
AMULE_SOURCE_DIR=/path/to/amule-source python3 tests/preflight.test.py
```

These regressions exercise the shell entry point with real aMule helper imports
and stop at a substituted browser probe; they do not launch a browser or daemon.
They cover missing dependencies and executable resolution across working directories.
The optional full application smoke test is still needed to establish queue acceptance.

Windows/macOS, native context-menu selection and peer file transfer are not
covered. Test failures and evidence must not be interpreted as success merely
because Chrome logged an external-handler launch.

## Release process

1. Complete the platform checks in [RELEASING.md](RELEASING.md).
2. Set the same version in `manifest.json`, `package.json` and
   `package-lock.json`, then merge the reviewed changes.
3. Create and push a `v<version>` tag in the upstream repository, for example
   `v1.0.0`. The tag must match both the manifest and npm package versions.
4. The release workflow checks out that tag, runs the DOM tests, builds the ZIP
   and attaches `ed2k-link-fixer.zip` to a GitHub release. It needs no npm token
   or Chrome Web Store credentials. Check the workflow and download the release
   asset before announcing availability.

The workflow never uploads to the Chrome Web Store. Publisher ownership and
store submission remain separate decisions for the maintainers.

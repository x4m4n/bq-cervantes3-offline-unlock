# BQ Cervantes 3: offline developer-firmware authorization

Install BQ's original developer firmware when its online authorization service is unavailable, using the stock reader's web browser and a small local HTTP server.

**Confirmed on one unregistered BQ Cervantes 3 running stock bqOS 6.0.3:** the browser wrote the authorization marker, the reader displayed “Device already authorised for hackers firmware installation,” and the owner reported a successful developer-firmware installation. No existing shell or hardware disassembly was required. Other models and firmware versions are untested.

## Why it works

The stock browser trusts a download filename supplied in the HTTP `Content-Disposition` header. It accepts filenames containing `.acsm` anywhere and joins them directly to `/mnt/public/`, without removing directory traversal components.

After you create an actual directory named `_bq_probe.acsm` in the internal USB-visible storage, the server supplies:

```http
Content-Disposition: attachment; filename="_bq_probe.acsm/../../private/hackers_e60q22_ok"
```

The browser writes the response body, exactly `ok`, to this path:

```text
/mnt/public/_bq_probe.acsm/../../private/hackers_e60q22_ok
                         ↓ resolves to
/mnt/private/hackers_e60q22_ok
```

USB only exposes public storage. The browser runs on the reader and, on the tested device, can write to private storage. **The reader writes the file; the server supplies its filename and contents.**

BQ's application checks for this marker before checking whether the device is registered. The normal online authorization flow creates the same marker. Once it exists, the original developer updater can be used.

See [the source walkthrough](docs/how-it-works.md) for pinned BQ source references and the distinction between authorization and firmware verification.

## What you need

- A BQ Cervantes 3 with access to its stock Web Browser. This method was tested on 6.0.3.
- A computer with Python 3 and a USB connection to the reader.
- A LAN accessible to both devices; the computer may use Ethernet and the reader Wi-Fi.
- A microSD card and the original Cervantes 3 developer **initial-installation** package for 6.0.3.
- A backup of your books/files and reliable power during installation.

The Python server uses only the standard library. It serves four fixed routes and cannot serve arbitrary computer files. Marker mode is disabled by default. When enabled, two separate buttons offer `hackers_ok` and `hackers_e60q22_ok`; use the [model/version compatibility table](docs/compatibility.md) to choose. Only the Cervantes 3 installation has been confirmed on a device.

## Steps

Follow the [complete installation guide](docs/installation.md). The short version is:

1. Back up the reader's USB-visible files. Create the empty directory `_bq_probe.acsm` at the root of its **internal** USB-visible storage, then safely eject and disconnect USB.
2. Start the server, replacing `192.168.1.100` with your computer's LAN IPv4 address:

   ```sh
   python server.py --bind 192.168.1.100 --port 8000
   ```

3. On the reader, open **Settings → Web Browser** and visit `http://192.168.1.100:8000/`. Download the public-storage probe. Reconnect USB and verify `bq_download_probe` exists in the internal drive root with the expected contents. Safely eject and disconnect again.
4. Stop the server with Ctrl+C and restart it with marker mode:

   ```sh
   python server.py --bind 192.168.1.100 --port 8000 --enable-marker
   ```

5. Visit the same page and select **Write hackers_e60q22_ok** for Cervantes 3. The other button, **Write hackers_ok**, is for older firmware/models listed in the compatibility table. Each button downloads only its named marker. Exit the browser and insert/reinsert a microSD card without an update folder, while the reader is running normally. Confirm the **already authorised** message, then stop the server.
6. Put the original `bqupdate` folder on the microSD root. Power off the reader, insert the card, hold Home and press Power. Release Power when the green LED comes on; keep Home held until the updater starts. Let installation finish without interruption.

On systems where the Python command is `python3` or `py -3`, use that instead of `python`.

## Preservation and limits

Writing the marker changes the local authorization state and leaves the stock firmware installed. Installing developer firmware subsequently replaces the stock software. A USB file backup is **not** a full firmware or internal-storage backup. This method does not provide a pre-installation shell or a complete rollback image.

BQ's original instructions state that developer firmware removes shop-purchased books and disables stock dictionaries. Back up what you can before installation. Use the initial-installation package for the correct model; stock restoration is a separate destructive procedure.

This project does not decrypt, patch, directly flash, or bypass the firmware signature. The encrypted installer was not extracted, and its exact write targets have not been independently audited. The successful installation is an owner report from one device, not a guarantee for every reader.

## Repository contents

- [`server.py`](server.py): fixed probe and opt-in marker responses.
- [Installation guide](docs/installation.md): commands, firmware links, checks and expected results.
- [How it works](docs/how-it-works.md): browser behavior and authorization source references.
- [Compatibility](docs/compatibility.md): marker selection by model and published firmware version.
- [Troubleshooting](docs/troubleshooting.md): network, download and updater problems.
- [Firmware findings](docs/firmware-findings.md): package hashes and OpenPGP metadata.

Run the local server checks with:

```sh
python tests/test_server.py
```

These checks cover the HTTP responses, marker gating and destination paths. They do not emulate a reader or run firmware.

## Credits and license

The method was derived from [BQ's published Cervantes application source](https://github.com/bq/cervantes) and tested by the reader's owner. BQ's source and firmware retain their respective licenses and ownership; neither is bundled here. The original Python server and documentation in this repository are licensed under the [GNU General Public License, version 3 or later](LICENSE) (`GPL-3.0-or-later`).

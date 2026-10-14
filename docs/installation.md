# Installation guide

Tested starting state: **unregistered Cervantes 3, stock bqOS 6.0.3, no shell**. The owner confirmed authorization and a successful developer update. Do not assume this guide applies to a Cervantes 4, another BQ model or another firmware version.

## 1. Back up and prepare

Connect the reader to your computer by USB and copy its visible books/files somewhere safe. This is a personal-file backup, not a full backup of firmware, private storage or calibration data.

Create an empty **directory**, exactly `_bq_probe.acsm`, at the root of the reader's internal USB-visible drive. Do not put it on the microSD card. Safely eject the reader and disconnect USB so its own software can access the storage again.

Charge the reader fully before installing firmware. BQ's original developer-program instructions state that installation removes shop-purchased books and disables stock dictionaries. See the [archived official instructions](https://web.archive.org/web/20200720044821/https://blog.bq.com/es/bq-ereaders-developers-program/).

## 2. Find the computer's LAN address

Connect the computer and reader to the same LAN. Ethernet on the computer is fine. Use its LAN IPv4 address, not a VPN address or `127.0.0.1`.

Windows:

```powershell
ipconfig
```

Linux:

```sh
ip -4 addr
```

macOS, for a typical Wi-Fi interface (interface names can differ):

```sh
ipconfig getifaddr en0
```

The remaining examples use `192.168.1.100`. Substitute your actual address in both the server command and the browser URL.

## 3. Run the public-storage probe

Open a terminal in this repository and start:

```sh
python server.py --bind 192.168.1.100 --port 8000
```

Use `python3` on systems that require it, or `py -3` on Windows. No packages need installing.

If the firewall asks, allow Python on your private LAN. Keep the server local; no router port forwarding is needed. The default bind address is loopback, so the explicit `--bind` argument is necessary for the reader to reach it.

On the reader, open its ordinary **Settings → Web Browser**, connect Wi-Fi and visit:

```text
http://192.168.1.100:8000/
```

Select **Download the harmless public-storage probe**. Wait for completion. Reconnect USB and check that `bq_download_probe` appears in the internal drive root, next to `_bq_probe.acsm`. It must contain:

```text
BQ browser download path probe: public storage only.
```

The file has a final newline and is 53 bytes. A download dialog alone is insufficient confirmation. If the file is absent or in a different location, troubleshoot before continuing.

Safely eject and disconnect USB again. Leave the directory in place.

## 4. Write the authorization marker

Stop the first server with Ctrl+C. Start marker mode:

```sh
python server.py --bind 192.168.1.100 --port 8000 --enable-marker
```

Visit the same page on the reader and select **Write hackers_e60q22_ok** for Cervantes 3. A second button, **Write hackers_ok**, supports the older source-defined marker; see [compatibility](compatibility.md) before using it on another model. Each button downloads one marker, not both. Wait for completion and exit the browser. Keep the download connection stable; the browser's error/cancel paths can remove the destination.

The `/marker` response supplies:

```http
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="_bq_probe.acsm/../../private/hackers_e60q22_ok"
Content-Length: 2
```

Its body is exactly `ok`, with no newline. The browser writes `/mnt/private/hackers_e60q22_ok` on the reader. This does not flash firmware.

While the reader is running normally, insert or reinsert an external microSD card **without a `bqupdate` folder**. Look for:

> Device already authorised for hackers firmware installation

This is the authorization confirmation. No serial-number trigger file or linked BQ account was needed on the tested device. If the message does not appear, stop here and troubleshoot; do not use an updater boot as the marker check.

Stop the server with Ctrl+C. It is no longer needed for installation.

## 5. Obtain the original initial-installation package

The package used in the confirmed installation was `hackers_update_Cervantes3_603.zip`:

- [Internet Archive collection](https://archive.org/details/bq-fnac-cervantes-dev-firmware)
- [Direct archived package](https://archive.org/download/bq-fnac-cervantes-dev-firmware/BQ/hackers_update_Cervantes3_603.zip)
- [Historical BQ-hosted package URL](https://storage.googleapis.com/otas/2017/eReaders/Cervantes3/hackers_update_Cervantes3_603.zip) (availability may change)

This repository does not contain the firmware. Use the **initial-installation** package, not a developer reinstall package or a stock restoration package. Extract it on the computer and check the file sizes and hashes in [firmware findings](firmware-findings.md).

Windows PowerShell, from the extracted package directory:

```powershell
Get-FileHash -Algorithm SHA256 .\bqupdate\update.img
Get-FileHash -Algorithm SHA256 .\bqupdate\update.asc
```

Linux:

```sh
sha256sum bqupdate/update.img bqupdate/update.asc
```

macOS:

```sh
shasum -a 256 bqupdate/update.img bqupdate/update.asc
```

Matching hashes establish correspondence with the files investigated and used here. They do not independently authenticate BQ's signature.

## 6. Install through the normal updater

Copy `bqupdate` directly to the microSD root:

```text
microSD root/
└── bqupdate/
    ├── update.img
    └── update.asc
```

There must be no extra enclosing folder. Do not rename, modify, decrypt or mix the two files with another package.

Safely eject the card. Power the reader off normally, insert the card, **hold Home and press Power**. Release Power when the green LED comes on; keep Home held until the update screen/process starts. Holding both buttons throughout boot is the separate external-boot gesture described by BQ.

Let the updater finish. Do not remove the card or interrupt power during installation. A blinking LED by itself does not prove progress. No reliable duration for the developer updater's “Preparing update” stage was established in this investigation; BQ's separate stock-restoration timing should not be treated as its timeout.

If a signature, decryption or model error appears, record the exact message and stop. Do not force a raw write or substitute a restoration image.

## 7. Check completion and clean up

After the reader boots normally, look for **Settings → Development**. The version number may still say 6.0.3; the developer options distinguish the edition.

Remove the update card after completion, or remove its `bqupdate` folder before ordinary use. The public `_bq_probe.acsm` directory and `bq_download_probe` file can also be removed through USB. The private authorization marker remains.

BQ documents developer USB networking at `192.168.4.1`, enabled through the Development settings. Enable and inspect it deliberately before attempting shell access. Use the resulting access to back up internal storage before further modifications; this would preserve the current developer installation, not reconstruct the previous stock state.

# Source walkthrough

## Evidence and scope

The source references below are pinned to BQ commit `17ba4f5bf7a9f8f3a2e1ca2fe79c0665ce0bccfe`. Its [version.h](https://github.com/bq/cervantes/blob/17ba4f5bf7a9f8f3a2e1ca2fe79c0665ce0bccfe/version.h) identifies `bqOS-6.0.3`. These files were inspected locally during the investigation.

The owner then confirmed both the authorization message and completion of the developer update on an unregistered Cervantes 3 running stock 6.0.3. The private file was not independently read back through a shell; the source, served response, authorization message and installation outcome support the conclusion that the marker write succeeded.

## 1. Public and private storage are different mounts

[StorageMx508.cpp, lines 89–105](https://github.com/bq/cervantes/blob/17ba4f5bf7a9f8f3a2e1ca2fe79c0665ce0bccfe/bqHAL/Storage/mx508/src/StorageMx508.cpp#L89-L105) maps the E60QH2 hardware branch used by Cervantes 3 to:

| Storage | Mount | Source-defined block device | Filesystem |
| --- | --- | --- | --- |
| Public | `/mnt/public` | `/dev/mmcblk0p4` | VFAT |
| Private | `/mnt/private` | `/dev/mmcblk0p7` | EXT3 |

These are source-defined mappings, not a partition table extracted from the encrypted update. No raw partition writes are needed for this method.

USB file transfer exposes public storage. That does not constrain the reader's own applications to the public mount.

## 2. The browser preserves a server-controlled path

[Browser.cpp, lines 414–442](https://github.com/bq/cervantes/blob/17ba4f5bf7a9f8f3a2e1ca2fe79c0665ce0bccfe/bqBrowser/src/Browser.cpp#L414-L442) extracts `filename=` from `Content-Disposition`. It strips quotes but preserves slashes and `..` components.

[Lines 1150–1164](https://github.com/bq/cervantes/blob/17ba4f5bf7a9f8f3a2e1ca2fe79c0665ce0bccfe/bqBrowser/src/Browser.cpp#L1150-L1164) use that name in preference to the URL filename. The download is accepted if it is a supported book filename **or contains `.acsm` anywhere**, case-insensitively.

[Lines 461–463](https://github.com/bq/cervantes/blob/17ba4f5bf7a9f8f3a2e1ca2fe79c0665ce0bccfe/bqBrowser/src/Browser.cpp#L461-L463) concatenate the public mount, a slash and the supplied name, then open that path for writing. There is no destination containment check at this point.

This is directory traversal through a download filename, commonly described as CWE-22. The fixed server uses it only for a public probe and the known authorization marker.

## 3. An existing `.acsm` directory satisfies the filter

The directory `_bq_probe.acsm` serves two purposes: its name passes the `.acsm` substring check, and it exists so the operating system can traverse it before processing `..`.

Creating this directory on the internal USB-visible drive makes these paths usable:

```text
Public probe:
/mnt/public/_bq_probe.acsm/../bq_download_probe
→ /mnt/public/bq_download_probe

Authorization marker:
/mnt/public/_bq_probe.acsm/../../private/hackers_e60q22_ok
→ /mnt/private/hackers_e60q22_ok
```

A nonexistent directory cannot simply be canceled by a following `..` during filesystem traversal. A regular file with the same name is also insufficient.

The final filenames have no extension. [Post-download processing](https://github.com/bq/cervantes/blob/17ba4f5bf7a9f8f3a2e1ca2fe79c0665ce0bccfe/bqBrowser/src/Browser.cpp#L591) handles a final `.acsm` extension differently; placing `.acsm` in the directory name avoids that branch. The server also uses extensionless URLs `/probe` and `/marker` to reach the relevant download handling.

## 4. The authorization flow ends in a local marker

[QBookApp.cpp, lines 3671–3709](https://github.com/bq/cervantes/blob/17ba4f5bf7a9f8f3a2e1ca2fe79c0665ce0bccfe/QBookApp/src/QBookApp.cpp#L3671-L3709) calls the original online authorization service and checks its response. On success, it writes exactly `ok` to the private marker. [Lines 3643–3668](https://github.com/bq/cervantes/blob/17ba4f5bf7a9f8f3a2e1ca2fe79c0665ce0bccfe/QBookApp/src/QBookApp.cpp#L3643-L3668) derive the expected response from the serial number and an embedded salt.

The SD-insertion handler [at lines 1537–1556](https://github.com/bq/cervantes/blob/17ba4f5bf7a9f8f3a2e1ca2fe79c0665ce0bccfe/QBookApp/src/QBookApp.cpp#L1537-L1556) first checks whether the marker exists. It displays the already-authorized message before reaching the registered-account condition `isLinked()`.

The marker download reproduces that local file, with this response body:

```text
ok
```

There is **no newline**: the body is two bytes, hexadecimal `6f 6b`. The application confirmation shown in this source checks existence; this project writes the original contents as well, rather than relying on an empty file.

## 5. The local server does not impersonate BQ

The reader visits a local HTTP URL entered by the owner. No BQ hostname redirection, account registration, serial number, service response token or TLS certificate is needed. The private service implementation was not available in the examined public repository, so its full original protocol was not reconstructed.

The server sends a filename and a body. The browser opens the destination and writes the bytes using its own filesystem permissions. It does not mount the private partition on the computer or expose it over USB.

## 6. Authorization and firmware verification are separate

The marker permits the normal installation workflow. It does not provide a firmware decryption key or signing key. The supplied firmware remains an unchanged encrypted OpenPGP message accompanied by a detached signature.

The recovery installer was not extracted. Its exact verification implementation and partition writes remain unverified. The owner-confirmed installation demonstrates that the original package was accepted on the tested device after the marker step.

The authorization step preserves the installed stock software. The subsequent developer installation changes it; a full original-firmware backup is a separate task.

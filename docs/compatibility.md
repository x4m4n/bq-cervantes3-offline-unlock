# Choose the authorization marker

Marker selection depends on **hardware model and firmware version**, not on a single version cutoff for every reader. Each server button downloads one file containing exactly `ok`, with no newline, to `/mnt/private` through the reader's browser.

| Published source / hardware | Button | Destination |
| --- | --- | --- |
| bqOS 5.0.0, 5.0.2 and 5.1.0 (all hardware branches in these revisions) | **Write hackers_ok** | `/mnt/private/hackers_ok` |
| Cervantes Touch (E606A2), Cervantes Touch Light (E60672), including matching Fnac models, in later checked revisions | **Write hackers_ok** | `/mnt/private/hackers_ok` |
| Cervantes 2013 (E60Q22), from bqOS 5.2.0 in the checked revisions | **Write hackers_e60q22_ok** | `/mnt/private/hackers_e60q22_ok` |
| Cervantes 3 (E60QH2), checked 6.0.1–6.0.3.1 and 7.0.1–7.0.2 source | **Write hackers_e60q22_ok** | `/mnt/private/hackers_e60q22_ok` |
| Cervantes 4 (E60QP2), checked 7.0.1–7.0.2 source | **Write hackers_e60q22_ok** | `/mnt/private/hackers_e60q22_ok` |

The checks covered published revisions 5.0.0, 5.0.2, 5.1.0, 5.2.0, 5.2.1, 5.2.2, 6.0.1, 6.0.2, 6.0.3, 6.0.3.1, 7.0.1 and 7.0.2. Version ranges in this table describe those checked revisions; they do not establish compatibility for unpublished releases, custom firmware or future versions.

**Device-confirmed result:** authorization and developer installation on one unregistered Cervantes 3 running stock 6.0.3. The other selections are derived from public source and have not been installation-tested by this project. A Fnac Touch Light owner reported a successful public probe on 5.1.0 but no authorization after downloading the Cervantes 3 marker; the corrected legacy marker still needs device confirmation.

## Where the split comes from

- [5.1.0 source](https://github.com/bq/cervantes/blob/9cd563895b5579804428164350083a53245f9a56/QBookApp/src/QBookApp.cpp#L1514-L1527) uses `hackers_ok` directly. Its [authorization success path](https://github.com/bq/cervantes/blob/9cd563895b5579804428164350083a53245f9a56/QBookApp/src/QBookApp.cpp#L3565-L3568) writes `ok` to the same marker.
- [5.2.0 source](https://github.com/bq/cervantes/blob/814ed831f74179dd83a6ae0fb09b95bc78ee5d74/QBookApp/src/QBookApp.cpp#L1521-L1529) introduces a hardware branch: E60Q22 uses `hackers_e60q22_ok`; other supported models retain `hackers_ok`. The same selection appears in 5.2.1 and 5.2.2.
- [6.0.3 source](https://github.com/bq/cervantes/blob/17ba4f5bf7a9f8f3a2e1ca2fe79c0665ce0bccfe/QBookApp/src/QBookApp.cpp#L1537-L1546) includes E60QH2 (Cervantes 3) in the newer-marker branch. Touch and Touch Light retain the legacy marker.
- [7.0.2 source](https://github.com/bq/cervantes/blob/dc7664ff4afbd57a8db227e940e3232dd6abf0fb/QBookApp/src/QBookApp.cpp#L1539-L1549) includes E60QP2 (Cervantes 4) in the newer-marker branch as well.
- [Hardware identifiers](https://github.com/bq/cervantes/blob/dc7664ff4afbd57a8db227e940e3232dd6abf0fb/bqHAL/Devices/inc/DeviceInfo.h#L37-L43) map the hardware branches to model names.

## Routes and confirmation

- `/marker-legacy`: `_bq_probe.acsm/../../private/hackers_ok`
- `/marker`: `_bq_probe.acsm/../../private/hackers_e60q22_ok` (the existing route is preserved)

Both routes require `--enable-marker`. Neither flashes firmware. Select the correct button, wait for the download, exit the browser and reinsert an empty microSD in the normal reader application. Look for the already-authorized message. A successful public probe alone does not establish private-storage write permission.

The inspected application authorization checks ignore the unrelated marker, so an earlier download of the other filename need not be removed for this check. Use the correct developer firmware for the exact model after authorization; this table is not a cross-model installation guide.

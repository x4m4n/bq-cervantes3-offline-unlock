# Troubleshooting

## The reader cannot load the page

- Use `http://`, not `https://`. This server provides plain HTTP.
- Use the computer's LAN address. `localhost` on the reader means the reader itself.
- Keep the server terminal open and check the listening address/port printed at startup.
- Confirm both devices can communicate on the LAN. Guest Wi-Fi, client isolation and some VPN configurations block local traffic.
- Allow the listener through the firewall for the private LAN; do not disable the firewall globally or forward the port from the internet.

The server prints requested paths. A page request in the log proves the reader reached it, not that any file write succeeded.

## The download succeeds but the probe file is missing

Check that `_bq_probe.acsm` is an actual directory at the **internal** drive root, not a file or a directory on the microSD. Eject/disconnect USB before using the reader browser.

Use the provided page and extensionless `/probe` URL. Check for the exact filename `bq_download_probe` in the internal drive root. Do not proceed solely on the download dialog or HTTP log. The public probe demonstrates this filename handling, but does not prove private-storage write permission.

## The marker endpoint returns 403

Marker mode is intentionally disabled by default. Stop the server and restart with `--enable-marker`, using the same bind address and port. This flag enables the two fixed marker routes `/marker` and `/marker-legacy`; the server accepts no arbitrary destination or body.

## There is no already-authorized message

Exit the browser and insert/reinsert a microSD card with no update folder while the normal application is running. The confirmation is triggered by SD insertion, not by reconnecting USB.

If the probe succeeded but authorization does not, record the model, installed stock version, download result and SD-insertion message. A patched browser, different hardware, filesystem permissions or deployed firmware differences may prevent the private write. Do not assume compatibility with another model from similar source alone.

Check the [marker compatibility table](compatibility.md). For example, bqOS 5.1.0 checks `hackers_ok`, so writing only `hackers_e60q22_ok` does not produce its authorization message.

## The updater remains on “Preparing update”

Keep reliable power connected and leave the microSD in place while assessing it. The blinking LED does not establish whether work is progressing. Record the elapsed time, exact screen text and any subsequent error. This project has no verified preparation-stage timeout or general safe-reset procedure.

Do not repeatedly interrupt an updater or try a stock-restoration package as an improvised fix. Restoration is a separate destructive operation. Seek device-specific recovery advice if the process remains unchanged for an unusually long time.

## The updater reports signature, model or decryption failure

Record the exact message. Check the package identity, hashes and card layout when it is safe to access the card again. Keep `update.img` and `update.asc` from the same original initial-installation package. The marker bypass does not bypass cryptographic verification or make other models' firmware compatible.

## What the server logs

The server logs the request method, path and Host header to its terminal. It does not request a serial number, account password or registration token. Do not publish logs without reviewing them for identifying addresses or paths.

Stop the server after authorization. There is no authentication on the listener; any client that can reach it can request its fixed responses. The server does not modify a reader merely because it receives a request: the requesting browser performs the download write.

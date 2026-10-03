# Firmware findings

The confirmed installation used the original initial-installation archive `hackers_update_Cervantes3_603.zip`. Its extracted image and signature matched the owner's supplied files byte for byte. The archive passed a ZIP CRC check.

| File | Bytes | Digest |
| --- | ---: | --- |
| `hackers_update_Cervantes3_603.zip` | 162,579,719 | SHA-1: `386e0803b919efebf23c83579f15e030ee3c46d1` |
| `bqupdate/update.img` | 162,552,715 | SHA-256: `250384600920c11b41f88d76c736ca9918b0eb667ac0be3be6d38ae74316d33f` |
| `bqupdate/update.asc` | 490 | SHA-256: `3278b1269995574d6a939b148083d30e659abee0275c2ca85bf1222068a9fc9e` |

The archive SHA-1 is included for correspondence with the mirror metadata. Use the extracted-file SHA-256 values for the checks in this guide. These are reference hashes, not independent proof of publisher authenticity.

## Container and signature

`update.img` is an encrypted OpenPGP message, rather than a directly mountable disk image:

- A tag-1 public-key-encrypted session-key packet starts at offset 0. It uses RSA and recipient key ID `01A45DDC4AE35FBD`; the encrypted MPI is 2048 bits.
- A tag-18 integrity-protected encrypted-data packet starts at offset 271. Its body starts at offset 277 and is 162,552,438 bytes long.
- `update.asc` contains a version-4 detached binary-document RSA/SHA-1 signature, issuer key ID `D21B76D322392161`, created 2017-11-26 23:41:26 UTC.
- The calculated signature hash prefix matched the stored prefix `283f`. This is only a 16-bit consistency check, **not full signature verification**.

No corresponding decryption secret key or trusted signing-key verification was obtained during the investigation. The encrypted payload, contained filesystems, installer scripts and exact partition-write targets were not extracted. Apparent filesystem signatures in ciphertext should not be treated as real partitions.

The browser marker method does not change these files. It enables the normal device updater workflow, and the owner reported that installation completed successfully.

## Recovery limits

BQ's archived instructions identify the first 10 MB of internal storage and the rescue partition as critical recovery data. USB-visible books are not a backup of those areas. This repository deliberately provides no raw-flash, repartitioning or factory-restoration commands.

Further modifications should start with a device-specific full backup once developer access is available. Such a backup captures the installed developer system; an exact pre-installation stock image cannot be recovered from a books-only backup.

Sources: [BQ application source](https://github.com/bq/cervantes), [archived official developer instructions](https://web.archive.org/web/20200720044821/https://blog.bq.com/es/bq-ereaders-developers-program/), [firmware archive](https://archive.org/details/bq-fnac-cervantes-dev-firmware). Binary metadata above comes from local inspection of the supplied files.

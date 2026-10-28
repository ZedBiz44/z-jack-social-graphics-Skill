# Private Save Receipt Contract

Use a receipt only after the executing agent's actual upload and separate metadata/content read-back. Keep the filled receipt private. Never invent facts to obtain a checker pass.

## Required contents

The JSON object has these fields:

- `expected`: non-empty strings `name`, `parent_id`, `drive_id`, `boundary_id`, `owner`, and `knowledge_key`, established from the request, live policy, and approved configuration before saving.
- `file`: the saved file's actual Drive GET fields `id`, `name`, `parents`, `driveId`, `mimeType`, `size`, `md5Checksum`, `webViewLink`, and `trashed`.
- `ancestors`: an ordered list of actual folder metadata from the direct parent through the approved scoped boundary. Each entry includes `id`, `name`, `parents`, `driveId`, and `mimeType`. Each child points to the next parent. The scoped boundary is not the whole Shared Drive.
- `verification`: true booleans `account_verified`, `policy_checked`, `metadata_read_back`, and `content_opened`, set only when the corresponding checks actually succeeded.
- `content_evidence`: a non-empty reference to the observed successful content-opening tool result. State what opened and where its evidence is recorded.
- `metadata_read_at`: the actual timezone-bearing ISO-8601 metadata read time, preferably UTC ending in Z.

## Run the local check

```bash
python3 scripts/check_save_receipt.py /actual/private/save-receipt.json --image /actual/local/graphic.png
```

The checker supports PNG, JPEG, WebP, and GIF. It checks local image magic, byte size, Drive MD5 matching, the intended filename/parent/Drive, ordered scoped ancestry, fresh read time, and the declared verification fields. Use names consistent with the Files & Folders Guide. Metadata older than 24 hours must be refreshed; do not backdate it. Read timestamps over five minutes into the future fail.

A missing Drive MD5 or unsupported format prevents this optional checker from passing. Perform an authorized downloaded-content comparison where appropriate and report the actual alternative check. Do not invent a checksum or weaken access to make a test pass.

## What a pass means

A pass means the supplied receipt is internally consistent with the supplied local image. It does not independently prove account authorization, policy approval, an upload, fresh API reads, or visual content inspection. Those facts must come from actual live tools and observed results.

The helper does not generate images, call Drive, upload files, change sharing, or grant any permissions. A failed receipt check does not authorize deletion, overwrite, or a blind re-upload. Preserve the work and investigate the affected discrepancy.

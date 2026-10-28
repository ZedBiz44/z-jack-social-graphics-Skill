# Quality and Test Checks

A successful graphic task requires both a usable image and a verified automatic save. A good local image alone is not full completion.

## Visual acceptance

- Jack's face matches the approved portraits, including blue eyes, recognizable nose/head shape, mature appearance, smile, and white/salt-and-pepper goatee.
- The default 2D inked, cel-shaded treatment is consistent across person and background, unless an explicit style change was requested. Facial likeness still applies after that change.
- Requested activity, pose, gaze, clothing, cap, props, setting, lighting, and framing are correct. No stale pointing, crossed arms, or plaid anchoring remains when those were not requested.
- Hands, limbs, and object interactions are credible. Important text and brand marks are accurate and readable at the intended size.
- Distinctive environment geometry follows the used real references. Illustrated examples may stylize scenery and screen content, but must not override contradictory real geometry.
- Image format and intended dimensions/aspect ratio are correct. No unrequested people, signs, props, or claims were added.

Inspect the actual output once against the used references. Correct one material failure with a focused revision and recheck; do not pursue endless subjective polish.

## Save acceptance

- The executing agent used its approved account and `z-files-folders` to establish the destination, knowledge key, filename, duplicate handling, and permission boundary.
- The image was uploaded and received a real file ID.
- A separate read-back confirms name, parent ancestry, Shared Drive, type/size, link, intended dimensions, and usable image content.
- A checksum or downloaded-content comparison supports binary integrity when available.
- If upload or verification fails, the retained local result is reported as `not-saved`; the full task is not marked complete.

## Real pilot evidence

Run only the tests authorized for the current assignment. Use `assets/pilot-request.md` as the representative brief without embedding its acceptance answers in the request.

Record native discovery/import versus explicit file-loading, package source commit and checksum, exact prompt, actual reference files supplied, tool path, generated output, visual findings, executing account/destination verification, Drive file ID/link, and upload read-back result. Keep account and folder details in private records.

A package import, synthetic unit test, local checksum pass, or another agent's working connection is not a real end-to-end success. If any required tool or access is absent, record that precise gap. Show the one-agent result to Jack and obtain approval before wider installation.

## Boundary cases

Check that actual-photo-only requests do not activate generation; requested clothing/pose changes override references; explicit style changes preserve likeness; missing identity input stops generation; ambiguous destination or unavailable binary upload prevents a save claim; and a timed-out write is inspected before retrying.

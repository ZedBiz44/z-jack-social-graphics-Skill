# Private Reference Library

This public repository contains instructions and a checksum manifest, not image binaries. Use private reference files only through an authorized private task. Never publish, embed, or link their bytes here.

## Active private payload: six images

The active private payload contains exactly these six images:

### Jack identity masters: four optimized files

- `assets/identity/jack-portrait-arms-crossed.jpg`: close facial identity and illustrated treatment.
- `assets/identity/jack-portrait-pointing.jpg`: close facial identity and illustrated treatment.
- `assets/identity/jack-standing-pointing-front.jpg`: mature full-body build and front-facing proportions.
- `assets/identity/jack-standing-pointing-relaxed.jpg`: mature full-body build and relaxed proportions.

Use these optimized active masters unchanged on each call; do not recompress them repeatedly. Full-size originals are retained separately in a private archive and their hashes are recorded in the manifest. Use a close portrait and a compatible full-body reference together when the confirmed live tool supports the required inputs. A reference image's clothing, pose, or expression is not an instruction unless the task requests it.

### Sole office environment: one file

- `assets/environments/office/office-main.jpg`: the sole active office architecture, furniture, camera, and framing authority.

`office-main.jpg` is the optimized 1152 × 864 full-frame master derived from the user-selected `CozyZedBizMountainLoftOffice.png` original. It is the only office environment input or active office comparison. Preserve its full original wide 4:3 view. The archived original remains byte-identical; the active master intentionally has new dimensions, encoding and checksum. Retired office originals and occupied-office comparison images remain outside the runtime payload; retain them privately rather than deleting them, but never attach, list as active, or publish them.

### Non-office scene/style comparison: one file

- `assets/approved-scenes/jack-deck-bbq.jpg`: an approved Jack build/style comparison for a BBQ scene.

This BBQ image is not an office input, office comparison, identity master, or automatic generation input. Use task-specific references for other settings; the office-base rule does not impose an office on BBQ, deck, pool, resort, or other scenes.

## Required reference discipline

- Pass actual image bytes through the live tool's supported image-input mechanism. A written filename, description, link, or prompt mention is not an image input.
- Record each call's exact input order and role. Describe an order only when those exact bytes were attached in that order.
- For an office desk request, use `office-main.jpg` as the one and only layout authority. Treat the request as inserting Jack into the supplied base, not permission to reconstruct or reframe the office.
- Do not attach a retired office image, an occupied-office example, or a prior generated office result as a competing base or comparison.
- If the actual tool cannot receive the required inputs, stop and report the capability gap. Do not substitute a generic textual Jack or an invented office.

## Office desk-test input order

Resolve SKILL_ROOT to the executing agent's actual installed skill directory. Expand the paths below to real absolute files before the call; do not pass placeholder paths.

Subject to confirmed support for all three actual image inputs, use this order exactly:

1. `{SKILL_ROOT}/assets/environments/office/office-main.jpg`: supplied office base; sole authority for the original wide 4:3 view, room, furniture, camera, and framing.
2. `{SKILL_ROOT}/assets/identity/jack-standing-pointing-front.jpg`: Jack's mature body build and proportions.
3. `{SKILL_ROOT}/assets/identity/jack-portrait-pointing.jpg`: Jack's facial identity, apparent age, eyes, smile, and goatee.

Keep the existing desk shape, drawers, end panel, position, monitors, windows, railing, surrounding objects, and chair location. Jack must occupy the existing simple grey upholstered chair with pale curved arms and a pale five-spoke base; do not replace it with a black mesh or modern metal chair, retain an empty chair, or add furniture. Only natural body or hand occlusion is allowed.

Make one actual-input-supported initial call and, only for one specifically identified material defect, at most one focused correction through the same verified route. Generation cannot be promised to preserve every source pixel; assess the required visual relationships instead.

## Integrity and privacy

`assets/reference-manifest.json` and `scripts/verify_reference_assets.py` check locally supplied private files; they do not establish visual quality or tool attachment. New outputs are outputs, not masters, and retain their actual extension. Never put image binaries, base64 payloads, private download links, account details, or private folder IDs in the public repository or public status records.

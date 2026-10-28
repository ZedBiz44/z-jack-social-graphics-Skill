# Private Reference Library

The public repository contains the instructions and reference checksum manifest, not actual reference images. A private distribution supplies the approved image payload. Keep originals unchanged.

## Identity references

The required files are:

- `assets/identity/jack-portrait-arms-crossed.jpg`
- `assets/identity/jack-portrait-pointing.jpg`
- `assets/identity/jack-standing-pointing-front.png`
- `assets/identity/jack-standing-pointing-relaxed.jpg`

Use a close-up portrait for facial identity and style. Use a full-body reference for proportions when needed. Select a relevant subset within the tool's actual input limit. The current pose and clothing override those shown in references. A requested style change does not allow facial drift.

## Office references

The required files are:

- `assets/environments/office/office-main-desk.webp`
- `assets/environments/office/office-wide-loft.png`
- `assets/environments/office/office-hallway-reverse.png`
- `assets/environments/office/office-desk-closeup.png`

The main desk view supports seated scenes. The wide loft view supports room layout and standing scenes. The reverse hallway view is the supplied real-layout reference. The close-up supports workstation details. Illustrated views may stylize exterior mountains, equipment, screen interfaces, or labels; do not use those invented details as proof about the real office.

Use new user-supplied environment images for their requested scenes. Do not force office architecture into a deck, resort, or other setting.

## Integrity and privacy

`assets/reference-manifest.json` lists the eight expected paths, byte sizes, roles, and SHA-256 values. Run `scripts/verify_reference_assets.py --skill-dir /actual/private/skill-folder` to check a local payload. This only checks the files and their integrity, not visual review or use by an image model.

Pass approved image files through supported image inputs within the authorized private task. Do not put personal images, base64 image data, private download URLs, or connected-account details into public GitHub files or status logs. A path mentioned in a prompt is not an image input.

The package builder can add the private payload from an explicitly supplied local directory. The source record keeps the technical commit and image-manifest checksum. A public code-only package remains unusable for reference-based generation until the payload is supplied and verified.

## Master control

Only Jack may approve a change to the permanent reference set. New graphics save automatically as outputs, not new masters. Preserve source images and their original extensions. Never replace, delete, or promote a master during routine generation. If identity images are inaccessible, stop rather than making a generic substitute.

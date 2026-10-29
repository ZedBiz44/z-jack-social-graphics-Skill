# Optimized reference masters — 2026-10-28

Jack authorized smaller active masters and the corresponding skill updates. The original six sources remain retained in the earlier private package; all six archived byte hashes were independently checked against the new manifest's original-source records.

## Change

- Created high-quality JPEG active masters with full framing, aspect ratios and artwork retained. Portraits are 1024 × 1024; office 1152 × 864; front body 768 × 1152; relaxed body 864 × 1152; BBQ 1152 × 768. JPEG quality 92, 4:4:4, Lanczos downsampling. The one RGBA source had fully opaque alpha, verified before conversion. No generative edit, crop or identity alteration.
- Required office/body/face inputs reduced from 5,840,937 to 983,933 bytes (83.2%). All six active images total 1,998,336 bytes.
- Updated active paths, manifest hashes, dimensions, archived-source provenance, platform transport guidance and package privacy exclusions. Historical records retain their original paths.
- Added a 2,000,000-byte office reference budget to the existing verifier and regression coverage for hash-valid oversized inputs. Base64 estimates include per-image padding and data-URI prefixes; prompt/JSON overhead remains additional.

## Verification and limits

- All 15 helper tests passed, including oversized-input rejection, retired-image rejection, checksums and package tests. Repository validator passed using a real PyYAML reader. The desktop runtime initially lacked YAML support; PyYAML was installed in a local validation-only dependency folder, outside the repository and agent runtime.
- Original and optimized artwork reviewed visually for retained framing and visible identity/detail. These are reference-master checks, not proof of future generated-image likeness.
- Built private candidate passed verification. On Roy, staged it outside the active skill and called the installed Krea adapter's request builder without any network/generation call. Old three-image set failed; new set produced three JPEG data URIs, decoded byte-for-byte to the selected masters in the correct order. Serialized test request: 1,312,122 bytes.
- No image generation, provider/default change, new account/key, active skill replacement, wider deployment or paid generation occurred. A real image-generation/save pilot remains a separate verification step; this is source/package and transport readiness, not Pilot Passed.
- Private package and retained-original links belong in the operational records, never this public repository.

Technical context: [Roy image-reference diagnosis](https://github.com/ZedBiz44/ZedBiz-hermes-ai-agents-vps3/issues/111). The human procedure is maintained in Notion, not duplicated here.

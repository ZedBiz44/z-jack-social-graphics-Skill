# Platform Requirements

A skill supplies instructions; it does not grant image, edit, storage, account, or provider capability. Verify the live platform immediately before an authorized task.

## Scope and private-payload boundary

Use only the agent and task scope authorized by the current assignment. Keep changing rollout or deployment status outside these evergreen runtime instructions.

The public source repository is not a complete private image package. Its active private payload is exactly six optimized images: four Jack identity masters, `assets/environments/office/office-main.jpg` as the one active office base, and `assets/approved-scenes/jack-deck-bbq.jpg` as a non-office comparison. Full-size originals, retired office originals and occupied-office comparisons remain outside runtime and must not be attached, published, or treated as active payload.

## Live-tool preflight

Before an image call, inspect current supported help/schema and record privately:

1. Which tool performs the image action and its actual image engine/provider.
2. Whether it accepts uploaded/reference image bytes, how many, and their accepted formats.
3. Whether it can create a new scene from separate images or, for an office insertion, can work from the supplied base image without inventing a replacement layout.
4. The actual input order/role mapping passed in the call and supported output handling.
5. Whether the executing agent's authorized file route can upload and read back an image binary.

State the image engine/provider separately from the agent's conversational model. Do not invent a model name, runtime path, permission, command, mask, reference-strength setting, or preservation guarantee.

## Reference-input rules

Reference-based generation requires actual supported image inputs, not text mentions of filenames. For the office desk test, the exact three-image sequence is valid only if all three are actually attached in this order:

1. `{SKILL_ROOT}/assets/environments/office/office-main.jpg`: the supplied base and sole authority for office architecture, furniture, camera, and framing.
2. `{SKILL_ROOT}/assets/identity/jack-standing-pointing-front.jpg`: body build.
3. `{SKILL_ROOT}/assets/identity/jack-portrait-pointing.jpg`: facial identity.

Treat the office request as placing Jack into the supplied `office-main.jpg` base. Preserve its full wide 4:3 framing, desk, chair, monitors, windows, railing, and surrounding objects as visual requirements; do not claim that a generative tool can guarantee pixel-exact preservation. Do not attach a retired office image, occupied-office comparison, or prior generated red-shirt office image.

If the live tool cannot accept this setup, stop and report the specific gap. Do not replace it with a generic Jack description, private file link, different unvalidated provider, or another agent's result. For non-office tasks, choose the relevant task-specific environment and keep the office-base restriction out of BBQ and other scenes.

## Attempts, editing, and failures

### Size and transport preflight

- Use the current optimized private package, not the archived source files. Run `python3 scripts/verify_reference_assets.py` from the skill folder. A hash or size failure means the package needs repair; it is not a reason to change providers or remove an input.
- The three office inputs must total at most 2,000,000 raw bytes. The verifier reports ordered inputs, raw bytes and estimated data-URI bytes. Base64 adds roughly one-third; serialized JSON, prompt and other fields add further bytes. Confirm the live request limit and image-count limit before sending.
- Hermes Krea was checked with a combined 3 MiB local-reference limit and four-reference limit. These are adapter limits, not a universal Krea contract; inspect the installed adapter/help if it changes. The optimized office set fits below those limits without dropping the office, body or face.
- A remote API cannot fetch a local filesystem path. Pass local files only to a tool documented to read them; otherwise use its supported data-URI or private upload mechanism. Do not put local paths in remote `image_url` fields. A private Drive viewing link is not a binary attachment.
- Use the agent's current supported Hermes launcher/tool environment. A legacy Python environment missing a library does not prove the active environment lacks it. Check the actual executing environment before proposing an installation. Never hard-code a versioned runtime directory in this skill.
- A payload-too-large error calls for checking the selected package and serialized request size first. An upload-authorization error is a separate storage permission problem. Nous generation authorization does not itself prove FAL storage authorization; do not request a new key before checking whether the existing route supports the smaller references directly.
- Smaller encoded files reduce transfer size. Lower pixel dimensions may reduce input-image charges where the provider bills by pixels; JPEG compression alone does not guarantee a cheaper generation. Verify the selected route's billing instead of repeating a fixed price.

### Generation attempts

Make one actual-input-supported initial output and, if one material defect is precisely identified, at most one focused correction through the same verified route. On broad identity/layout failure, missing capability, or a persistent material defect, stop and report facts. Do not represent a prompt, local file, or another agent's result as the executing agent's successful test.

Do not quietly swap provider/image engine, change an agent's default model, install a runtime, add credentials, create an OAuth connection, or buy a service to obtain an output. A different engine remains unvalidated until Jack approves and tests that route.

Keep image binaries, private folders, account IDs, upload receipts, and private payload locations out of repository files and public logs. A passing result still requires the authorized binary save and independent read-back; otherwise report it as `not-saved`.

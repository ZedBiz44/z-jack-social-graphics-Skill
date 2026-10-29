# Platform Requirements

A skill supplies instructions; it does not grant image, edit, storage, account, or provider capability. Verify the live platform immediately before an authorized task.

## Scope and private-payload boundary

Use only the agent and task scope authorized by the current assignment. Keep changing rollout or deployment status outside these evergreen runtime instructions.

The public source repository is not a complete private image package. Its active private payload is exactly six images: four unchanged Jack identity masters, `assets/environments/office/office-main.png` as the one active office base, and `assets/approved-scenes/jack-deck-bbq.png` as a non-office comparison. Retired office originals and occupied-office comparisons remain outside runtime and must not be attached, published, or treated as active payload.

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

1. `{SKILL_ROOT}/assets/environments/office/office-main.png`: the supplied base and sole authority for office architecture, furniture, camera, and framing.
2. `{SKILL_ROOT}/assets/identity/jack-standing-pointing-front.png`: body build.
3. `{SKILL_ROOT}/assets/identity/jack-portrait-pointing.jpg`: facial identity.

Treat the office request as placing Jack into the supplied `office-main.png` base. Preserve its full wide 4:3 framing, desk, chair, monitors, windows, railing, and surrounding objects as visual requirements; do not claim that a generative tool can guarantee pixel-exact preservation. Do not attach a retired office image, occupied-office comparison, or prior generated red-shirt office image.

If the live tool cannot accept this setup, stop and report the specific gap. Do not replace it with a generic Jack description, private file link, different unvalidated provider, or another agent's result. For non-office tasks, choose the relevant task-specific environment and keep the office-base restriction out of BBQ and other scenes.

## Attempts, editing, and failures

Make one actual-input-supported initial output and, if one material defect is precisely identified, at most one focused correction through the same verified route. On broad identity/layout failure, missing capability, or a persistent material defect, stop and report facts. Do not represent a prompt, local file, or another agent's result as the executing agent's successful test.

Do not quietly swap provider/image engine, change an agent's default model, install a runtime, add credentials, create an OAuth connection, or buy a service to obtain an output. A different engine remains unvalidated until Jack approves and tests that route.

Keep image binaries, private folders, account IDs, upload receipts, and private payload locations out of repository files and public logs. A passing result still requires the authorized binary save and independent read-back; otherwise report it as `not-saved`.

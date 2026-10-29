---
name: z-jack-social-graphics
description: Create or revise graphics featuring Jack with approved face/build references, scene checks and automatic Drive saving. Exclude actual photographs.
---

# Z Jack Social Graphics

Create the requested graphic of the same approved Jack, check both the person and the physical scene, and save it automatically. A recognizable generic man or an impossible desk/chair arrangement is a failed result.

## Scope and authority

- Use for illustrations, avatars, banners, lifestyle scenes, promotions and other created graphics that include Jack. Do not trigger merely to use an actual photograph Jack selected; real photographs can still be authorized reference inputs.
- Preserve the approved face, apparent age, eyes, smile, goatee, head-to-body proportions, shoulder width, torso and waist build. Do not slim, bulk up, make younger, exaggerate muscles or replace him with a generic man.
- Keep Jack's proven colorful 2D comic-book caricature style: bold clean black ink outlines, vibrant cel shading and rich saturated colors, matching the approved examples rather than inventing a new treatment. Change style only when requested.
- The current request controls activity, clothing, expression, pose, gaze, setting, season and lighting, not a different face or build. Never copy crossed arms, plaid clothing or pointing unless appropriate to the request.
- Default to a grey cap with readable blue ZedBiz lettering unless requested attire overrides it. Do not add unrelated people, furniture, props, claims, signage or brand marks.
- Saving a graphic never promotes it to a permanent identity master. Keep original references unchanged and obtain Jack's approval for master changes.

## Load the working instructions

- Load `z-files-folders` for approved access, ownership, naming, placement and verified saving; load `z-agent-communication` for all human-facing wording. Use [the companion source record](references/companion-skills.md) if needed. Stop affected actions if required guidance is unavailable.
- Read [reference roles and scene examples](references/reference-library.md), [the prompt templates](references/prompt-template.md) and [the visual rejection checks](references/quality-checks.md) before generation.
- Read [platform and image-tool requirements](references/platforms.md) before using image or Drive tools. A skill adds neither capabilities nor account permissions.
- Follow [the operational SOP](https://app.notion.com/p/407a3e33d58180ad8945dc54a67574aa). `z-ai-skill-developer` manages authorized development and staged release, not ordinary image creation.

## Prepare the request and destination

- Establish the requested scene, activity, clothing, gaze, pose, props, format and owner. Ask only for details that prevent correct or authorized work; do not make Jack relay an assignment the agent can execute itself.
- Follow the live [folder structure](https://www.notion.so/386a3e33d58180ea96fbc50b60102fe2) and [Files & Folders Guide](https://www.notion.so/3a9a3e33d58180548f4af69e804dcdfc). A user-specified destination still requires ownership/access verification; do not maintain another folder map here.
- Verify the executing agent's approved connection and binary upload/read-back ability. Keep private accounts, folder IDs and receipts outside public code.
- Include the executing agent's readable name in every new graphic filename, with a useful topic, date and version, using the companion's naming rules. Example: `jack-desk-black-golf-pointing-terry-2026-10-28-v03.png`. Match the extension to the actual image bytes. This is file attribution, not text to draw on the image.
- Check for existing names before writing; choose a new clear version rather than overwriting an original.

## Choose the scene route and image inputs

- For Jack's recurring loft office, use only `assets/environments/office/office-main.jpg`, the optimized full-frame master derived from the selected CozyZedBizMountainLoftOffice original, as the fixed scene base. Insert Jack into its existing chair through the verified image-edit/reference interface; do not freely reconstruct the office.
- Keep that image's full wide framing, camera, desk shape/drawers/end panel, simple grey upholstered chair with pale curved arms and pale five-spoke base, chair position, monitors, windows and railing. Do not zoom closer, crop the setting, substitute a black mesh chair, or import another office view or prior output. Preserve unchanged surroundings; do not promise pixel-identical generative preservation.
- Retired office views and occupied-office comparison pictures are not active references, even when a cache or older package still contains them. Load only the current six-image manifest. Original sources remain retained outside the installed package.
- For a new setting, activity or composition, use reference-based new-scene generation. Keep Jack's short prompt structure; do not require an already-occupied picture to create new scenes.
- For a small change to an approved compatible picture, an image edit may preserve more of the correct scene. Use it only when the actual tool accepts the base image for editing. Do not confuse an edit test with proof that new-scene generation works.
- For every route, explicitly assign each actual input its role: primary environment/layout, character face, body/build, optional prop, or approved style/comparison. Choose one primary layout view; do not blend inconsistent desk shapes or camera angles.
- For a visible seated or standing person, include an approved proportion reference as well as a clear face reference within tool limits. If a single approved scene supplies both, identify it clearly. Do not quietly drop a required role to fit an input limit.
- Use [the private manifest](assets/reference-manifest.json) and [reference verifier](scripts/verify_reference_assets.py) to check package files. Integrity checks do not prove the image model received or used those images.
- Use the optimized active masters as-is. Run `python3 scripts/verify_reference_assets.py` from the installed skill folder before generation; it checks hashes and the three-image office set's 2,000,000-byte budget. Check the live tool's image-count, raw-byte and encoded-request limits too. See [size and transport rules](references/platforms.md). Do not load archival originals, repeatedly recompress, drop a required reference, or seek a new key to work around an oversized request.
- Pass actual image bytes/files through supported image inputs in the stated order. A filename, description or vision summary alone is not a reference input. If required inputs cannot reach the generator, stop rather than inventing Jack.
- Confirm the actual image engine and supported interface. The agent's chat model is not necessarily its image engine. Do not silently switch providers, change defaults, add credentials or install services to get a picture out.

## Build and generate

- Use the short template: finished-picture description, mapped environment, character, attire, pose/activity, art style and appropriate lighting. Keep process rules and the review checklist outside the artistic prompt.
- Add only the task's necessary counts and physical relationships: who occupies which item, body support, object placement and believable contact. For this single-person desk test: one occupied existing chair at the working side, no extra chair/desk, and no desktop or edge passing through the stomach/torso.
- Apply the requested gaze rather than always facing the camera. Match lighting to the actual scene rather than copying timber-wall wording into unrelated places.
- Use the current supported tool schema and the approved existing service route. Record image-engine/model and actual input roles privately so the result can be repeated.
- Produce one initial image, retaining the source prompt and output. Do not treat a success response without a real image as completion.

## Reject visual failures before delivery

- Open the actual result and compare it with the request, supplied identity/build inputs, primary layout view and approved scene examples. Use [the visual checklist](references/quality-checks.md) and state what is uncertain rather than inventing measurements or a perfect-match score.
- Fail changed facial character/build, wrong requested pose/attire, extra or unsupported chairs, wrong desk layout, impossible hands, or furniture passing through the body. For the loft office, also reject a redesigned desk/chair or changed camera/framing; a plausible workstation alone does not pass. Ordinary foreground occlusion is not the same as impossible intersection.
- Check counts, occupancy, support and body/object boundaries before small decorative details. A nice background, readable cap or correct shirt does not excuse a bad physical scene.
- If one focused material defect remains, make at most one targeted correction in the same verified route. Name the actual defect and preserve only elements that are already correct; do not instruct the tool to preserve a broken desk arrangement.
- Recheck the corrected result against the complete checklist. If it still fails, or identity/layout is broadly broken, retain the attempt, report the concrete problem and stop. Do not run repeated variations or label a failed picture finished.

## Save automatically and finish

- Automatically save a passing graphic with the agent-attributed filename using `z-files-folders`; do not add another approval step for a routine authorized save. Save social, website-only and reusable work in their owner-appropriate homes under the live guide.
- Use the executing agent's own approved connection to read back returned file ID, name, parent ancestry, Shared Drive, type, size, dimensions and usable image content. Verify content/hash when supported.
- Follow [the private receipt contract](references/save-receipt.md); [the receipt checker](scripts/check_save_receipt.py) checks supplied facts, not whether an upload or visual review actually happened.
- After a timed-out upload, inspect the expected folder/file ID before retrying. Stop after three unsuccessful attempts at the same temporary operation. If saving is unverified, preserve the local output as not-saved and report the real issue.
- Keep failed attempts separate from completed deliverables. Never overwrite/delete originals, change sharing, publish, schedule, set up OAuth, add paid services or deploy to other agents during routine image work.
- Return the verified Drive link, filename, dimensions and actual check result in plain language. Report failures honestly. Record technical work in GitHub and append activity to the current Notion daily journal without putting private image binaries in public code.
- Finish only when the graphic meets the request and its automatic save is verified. Jack approves wider rollout after a real one-agent result; do not claim all-platform compatibility from a package check.

## Authorized build resources

- Use [the package builder](scripts/build_package.py) only for authorized builds. Public code alone is not reference-ready; include and verify the private approved payload.
- Use [the pilot request](assets/pilot-request.md) as a test, not a permanent pose/clothing default. Keep source commit, private package hash and installed-file checks together.

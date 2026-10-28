---
name: z-jack-social-graphics
description: Create or revise any graphic featuring Jack with consistent likeness and style, reference images, and automatic Shared Drive saving. Exclude actual photographs.
---

# Z Jack Social Graphics

Use for any created graphic that needs Jack in it. Preserve his likeness, follow the requested scene, and automatically save the completed graphic through the approved ZedBiz file process.

## Scope and authority

- Apply to illustrations, avatars, banners, lifestyle scenes, promotional graphics, and other generated graphics containing Jack.
- Do not activate merely to use an actual photograph Jack has chosen. Real photos may still be reference inputs when a generated graphic is requested.
- Preserve Jack's facial identity in every style: recognizable mature face, bright blue eyes, warm smile, and short white/salt-and-pepper goatee.
- Default to polished colorful 2D comic illustration, clean black outlines, vibrant refined cel shading, natural proportions, and warm lighting. Change style only when Jack explicitly requests it.
- Let the current request override reference-image pose, clothing, activity, expression, lighting, season, framing, and setting. Never carry over pointing or crossed arms unless requested.
- Default to a grey cap with readable blue ZedBiz lettering unless the requested attire overrides it.
- Do not invent extra people, props, signage, claims, or brand markings.
- Do not add, replace, or promote a permanent reference master without Jack's approval. Saving an output does not make it a master.

## Load the required guidance

- Load `z-files-folders` for file placement, names, approved access, and upload verification.
- Load `z-agent-communication` for all human-facing wording.
- Use [the companion source record](references/companion-skills.md) to locate the correct versions. If required guidance is unavailable, stop the affected action rather than inventing it.
- Read [the reference library](references/reference-library.md), [prompt template](references/prompt-template.md), and [quality checks](references/quality-checks.md) when creating or revising a graphic.
- Read [platform requirements](references/platforms.md) before using platform-specific image or Drive tools.
- Use [the Notion SOP](https://app.notion.com/p/407a3e33d58180ad8945dc54a67574aa) for the operational procedure. `z-ai-skill-developer` owns authorized development, validation, and staged release, not routine image work.

## Prepare the task

- Parse the requested activity, owner, destination use, image format, scene, pose, gaze, attire, props, message, and lighting. Ask only for a missing detail that prevents a correct or authorized result.
- Before generation, use `z-files-folders` to establish the approved account, owner-specific folder boundary, applicable knowledge key, filename, existing-item check, and write capability.
- Check the live [Z-Knowledge Folder Structure](https://www.notion.so/386a3e33d58180ea96fbc50b60102fe2) and [Files & Folders Guide](https://www.notion.so/3a9a3e33d58180548f4af69e804dcdfc). Do not maintain a second hardcoded folder map here.
- Keep account IDs, folder IDs, credentials, private reference locations, and save receipts in private runtime configuration or records, never in the public repository.
- Confirm the current tool can actually consume reference images and produce an image. Skill installation grants neither image generation nor Drive access.

## Select and supply references

- Use the approved close-up portraits for face and style. Use full-body references for proportions when relevant. Choose a relevant subset within the actual tool's image-input limit.
- Classify inputs as character, environment, prop, or style. Current real environment photos control geometry; illustrated environment references guide framing and treatment.
- Preserve distinctive architecture and major object relationships. Do not treat invented scenery or tiny screen interfaces in illustrated examples as real-world facts.
- Pass actual image files as supported image inputs to the generation/editing tool. Mentioning filenames in a text prompt does not enforce likeness.
- If identity inputs cannot be accessed or passed to the tool, stop generation and explain the missing capability. Never substitute a generic man or recreate a master from memory.
- If an optional scene reference is missing, use an alternative only when the request permits it and state the limitation.
- Run [the reference verifier](scripts/verify_reference_assets.py) against [the manifest](assets/reference-manifest.json) when checking a local package. Hash verification is not visual inspection.

## Generate and check

- Build the prompt from the current request using the prompt template. Explicitly override stale reference poses and clothing.
- Use the supported native tool schema and approved connection. Check current help rather than inventing commands, model names, permissions, or upload methods.
- Confirm an actual image output was produced. A prompt, package, or successful tool call without an image is not a generated graphic.
- Perform one clear visual check against the request and used references: facial likeness, consistent style, correct activity/attire, recognizable environment, credible hands/props, required text, and format.
- A style override does not permit facial drift. Required brand wording must remain readable and accurate.
- If a material defect makes the graphic unusable, make one focused correction and recheck. Preserve good elements rather than redesigning the whole image for subjective polish.
- If a material defect remains, retain the work and explain it. Do not label a failed image as a completed deliverable.

## Save automatically and verify

- Automatically save each completed task graphic using `z-files-folders`. Do not ask Jack for separate permission before a routine save or require a draft label unless the assignment calls for one.
- Keep completed social graphics in the owner-appropriate social-graphics home, website-only graphics in its website home, and reusable graphics in its general graphics home under the live guide.
- Never overwrite or delete an original. Reuse the correct existing item or choose an informative version after checking duplicates.
- After upload, obtain the returned file ID and independently read back its metadata and usable image content through the executing agent's own approved connection.
- Verify name, parent ancestry, Shared Drive identity, image type/size, intended dimensions, and accessible content. Compare a supported checksum or downloaded content when appropriate.
- Follow [the private receipt contract](references/save-receipt.md) and optionally run [the receipt checker](scripts/check_save_receipt.py). The checker only examines supplied facts; it cannot prove an upload or visual inspection happened.
- After a timed-out write, inspect the returned ID and expected folder before retrying. Stop after three unsuccessful attempts at the same operation.
- If saving cannot be verified, preserve and return the local image as `not-saved`, explain the actual failure, and state what access or decision is needed. Do not call the task complete.

## Limits and completion

- Routine graphics work does not authorize public posting, scheduling, sharing changes, source deletion, runtime installation, new OAuth setup, new paid services, or broader agent deployment.
- If a new material risk or scope change appears, stop that action, explain the options, and obtain Jack's decision before proceeding.
- Return the graphic, verified Drive link, and dimensions in clear language. Mention only actual checks and important limitations.
- Record technical changes and failures in the relevant GitHub issue; append the activity and result to the current Notion daily journal. Keep business image binaries in Drive, not GitHub.
- Finish only when the graphic meets the request and its automatic save has been verified. A local checksum, package check, or another agent's connection is not a real end-to-end test.

## Build and pilot resources

- Use [the package builder](scripts/build_package.py) only for authorized builds. A code-only public download is not generation-ready until its private reference payload is supplied and verified.
- Use [the pilot request](assets/pilot-request.md) as a test input, not a permanent pose or clothing preference.
- Apply `z-ai-skill-developer` validation and one-agent testing before wider installation. Preserve the approved source version and package checksum.

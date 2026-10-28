# Platform Requirements

A skill supplies instructions, not capabilities or account permissions. Verify the executing platform's actual image inputs, generation, file access, Drive actions, and discovery before relying on them.

## ChatGPT

OpenAI's [Skills in ChatGPT guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) describes eligible Business, Enterprise, Healthcare, and Edu access subject to product and workspace settings. Check the live interface rather than assuming the account qualifies.

When available, use Plugins > Skills > Create > Upload from your computer. Record the actual scan/import state, including Needs Review or Blocked. Installing a package does not grant image generation or Drive write actions.

Load the required companion guidance through approved installed skills or an authorized file/source-reading route. Verify actual reference-image bytes enter the image-capable tool. Extracting filenames from an archive is not visual image input.

The [Google Drive app guide](https://help.openai.com/en/articles/10948259-google-drive-app-with-sync) makes actions dependent on plan, workspace settings, and Google permissions. Verify that this connection can upload the generated binary image, not merely search metadata or create a text document. Respect platform-required confirmations even though this skill does not add a routine per-output approval gate.

If native skill import is unavailable, an explicitly authorized file-loading trial may test instructions only. Record it as such, not native discovery or full compatibility. If image input or binary saving is unavailable, report the incomplete capability rather than passing the test.

## Codex and other agent runtimes

Keep shared frontmatter limited to `name` and `description`. `agents/openai.yaml` provides optional UI metadata for supported OpenAI surfaces; it does not install a skill by itself.

For OpenClaw, Hermes, or another runtime, inspect its current skill creator, discovery path, image-tool schema, approved reference access, and private Drive configuration before an authorized installation. Do not invent runtime paths, accounts, providers, commands, or permissions. A supervisor's working connection does not prove the tested agent works.

## Tool and spending limits

Use supported native tools through the approved account and within the current task's authority. Do not install runtimes, create OAuth connections, add paid services, change sharing, post publicly, or remove originals during routine graphics work. Stop after three failed attempts at the same temporary operation, inspecting timed-out upload results before retrying.

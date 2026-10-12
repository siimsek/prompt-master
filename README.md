# Prompt Master

Prompt Master turns a rough request into a clear, tool-aware prompt. It is packaged as an [Agent Skills](https://agentskills.io/) skill: one `SKILL.md` with optional references, designed to travel across products that implement the format.

It helps write, improve, repair, explain, split, and adapt prompts for chat models, coding agents, research assistants, image and video tools, audio, 3D, and workflow builders. It does not take over the underlying task.

## Install

### Build the one ZIP

Requires Python 3.9 or later; there are no third-party dependencies.

```bash
python3 scripts/package_skill.py
```

The command builds and validates `dist/prompt-master.zip`. **Use this same ZIP** for supported Skills uploaders and ChatGPT's **Plugins → Upload plugin** flow. It contains one top-level `prompt-master/` folder with a directly loadable `SKILL.md`, its references, a plugin manifest, and the plugin's standard `skills/prompt-master/` copy. The duplicate skill file lets a single archive satisfy both package layouts.

### Platform support

| Surface | Install path | Notes |
| --- | --- | --- |
| ChatGPT Plugins → Upload plugin | Upload `dist/prompt-master.zip`. | The plugin manifest is inside the archive's only top-level folder. Plugin upload is shown when available and requires an eligible workspace role. [OpenAI packaging guide](https://developers.openai.com/plugins/build/plugins) · [Upload access](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt) |
| ChatGPT Skills | Use the same ZIP through **Plugins → Skills → Create → Upload**. | ChatGPT scans the skill before it becomes available. [OpenAI Skills guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) |
| Gemini app Skills | **Settings → Skills → Upload** and select the same ZIP. | Gemini accepts a ZIP containing a main folder with `SKILL.md`; feature availability can vary by account and surface. [Google guide](https://support.google.com/gemini/answer/17094296?hl=en) |
| Other Agent Skills clients | Upload the same ZIP if supported, or extract `prompt-master/` and install that folder using the client's documented method. | It contains the standard `SKILL.md` plus its reference files. For example, Claude Code loads skills from a documented skills directory. [Agent Skills format](https://agentskills.io/) |
| OpenAI API | Upload this ZIP as a skill package. | The archive has one top-level skill folder. [OpenAI API guide](https://developers.openai.com/api/docs/guides/tools-skills) |
| Tools without skill or plugin loading | Paste [`install/portable-instructions.md`](install/portable-instructions.md) into system, project, or custom instructions. | Add relevant reference files if the product supports attachments. |

If the Plugins uploader still reports an error, confirm that the upload flow is available to your account or workspace. OpenAI currently limits plugin upload to users with the required workspace access. The old `prompt-master.zip` contained only the skill layout; rebuild it with the script above to get the combined package.

## Use

Ask naturally and name the target tool when you know it:

```text
Write a prompt for Cursor to refactor my auth module.
```

```text
Fix this prompt for an image edit in Gemini. Keep the subject and lighting unchanged.
```

```text
Turn this feature request into a scoped task for a coding agent. Ask me if key details are missing.
```

Prompt Master asks a short clarification only when a missing detail would materially change the prompt. It adapts to the target surface, avoids unsupported model claims, and returns one copyable prompt unless you ask for variants or a sequence.

## Coverage

The skill contains capability-based guidance for:

- Chat and reasoning models, including Claude, ChatGPT/GPT, Gemini, Grok, Qwen, DeepSeek, MiniMax, Llama, Mistral, and local models.
- Coding and autonomous agents, including Codex, Claude Code, Cursor, Windsurf, Copilot, Cline, Antigravity, Devin, and SWE-agent.
- Research, image generation and editing, video, voice, 3D, app generation, and workflow automation.

Tool names are examples, not a promise that each product supports native Skills or a particular feature. Exact model names, controls, and syntax are included only when relevant and verified against current provider documentation.

## Files

- `SKILL.md` — portable core workflow and safety rules.
- `references/platforms.md` — adapting prompts by target surface and capability.
- `references/templates.md` — 13 task templates, loaded only when relevant.
- `references/patterns.md` — common prompt problems and repairs.
- `install/portable-instructions.md` — copy/paste fallback for products without Skills.
- `scripts/package_skill.py` — validates skill metadata and references, then builds the single combined ZIP.

## Updating the skill

Keep shared behavior in `SKILL.md`, durable tool guidance in `references/platforms.md`, and task structures in `references/templates.md`. Verify fast-changing model and product claims against official sources before adding them. Rebuild the archive with `python3 scripts/package_skill.py`.

## License

[MIT](LICENSE)

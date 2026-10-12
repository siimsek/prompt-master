# Platform and Capability Guide

Use this guide to adapt a prompt to the target's interaction surface and task. Product names and features change; the guidance below focuses on durable differences. Do not assume that two products using the same model expose the same tools or controls.

## Choose the surface first

- **Consumer chat app:** Give behavioral instructions the user can paste into chat or saved instructions. Do not describe API parameters or agent permissions that the app does not expose.
- **API or hosted agent:** Separate prompt text from configurable parameters, tools, and structured output settings. Include a schema only when the user needs machine-readable output and the target supports it.
- **CLI, IDE, or coding agent:** Specify the goal, relevant repository context, file or task scope, constraints, verification evidence, and stop conditions. Request inspection before edits when needed. Do not assume every agent can enforce a permission boundary written in a prompt.
- **Autocomplete assistant:** Anchor the request at the exact file, function, signature, or comment where completion should occur. State input/output behavior and edge cases compactly.
- **Generator or workflow builder:** Name the desired artifact, platform, stack or connected apps when relevant, user-visible behavior, required fields, and what counts as complete. Avoid requesting unlisted features.

## Chat and reasoning models

Applies to Claude, ChatGPT / GPT, Gemini, Grok, Qwen, DeepSeek, MiniMax, Llama, Mistral, and other hosted or local chat models.

- For ordinary chat models, use a direct task statement with only the context and constraints that affect the answer.
- For reasoning-oriented models, state the problem and requested result. Do not ask for hidden reasoning or add a long artificial reasoning script; ask for concise evidence or checks if auditability matters.
- For long-context or multimodal tasks, identify the provided files, images, audio, or video and say what to use them for. Do not assume an attachment is available unless the user will provide it.
- For structured output, define the exact fields and valid values. Use a JSON schema only on a surface that supports schema-constrained output; otherwise give a short example.
- For local model runners such as Ollama, ask for the exact model only when its identity changes the prompt. Keep instructions simple and distinguish a reusable system prompt from a one-time user prompt.

## Coding and autonomous agents

Examples include Codex, Claude Code, Cursor, Windsurf, GitHub Copilot, Cline, Antigravity, Devin, and SWE-agent.

- Name the desired change and provide available paths, current behavior, stack context, and acceptance criteria. Do not fabricate repository facts; ask the agent to inspect the project when they are unknown.
- Bound edits to the relevant files or directories when the user has a scope constraint. State excluded areas only when they matter.
- Ask for a concise summary of changed files and evidence from checks that were actually run. Do not tell an agent to claim tests passed without running them.
- For autonomous or computer-use agents, specify actions that need user approval, such as purchases, submissions, messages, deletion, deployment, or external writes. Stop before such an action if the target cannot obtain approval itself.
- For multi-step work, define checkpoints and a stopping condition. Split the task into sequential prompts only when stages depend on earlier output or the user asks for that.

## App and interface generators

Examples include Bolt, v0, Lovable, Figma Make, and Google Stitch.

- Describe the audience, purpose, key screens or components, visual direction, responsive needs, and expected interactions.
- Name the stack or integration only when required. State whether the target should implement the design or produce a mockup/specification.
- Avoid inventing platform-specific component names, framework defaults, or generation controls. Keep the feature list limited to the requested outcome.

## Research and web search

Examples include Perplexity and research modes in general-purpose assistants.

- Specify whether the user wants discovery, synthesis, comparison, or a recommendation.
- For current or factual claims, request web research and citations when the target supports them. Ask it to separate sourced facts from inference and to state uncertainty.
- Define date range, geography, source quality, and comparison criteria only when they affect the answer.

## Images and visual editing

Examples include Midjourney, image generation or editing in ChatGPT and Gemini, Stable Diffusion, and ComfyUI.

- Detect whether the request is a new generation or an edit to an existing image. For edits, describe only what changes and what must remain stable; remind the user to attach the reference when necessary.
- For generation, describe subject, action, setting, style, composition, lighting, color, and aspect ratio as relevant. Prioritize the details that matter instead of filling every field.
- Use negative prompts, weights, parameter flags, or separate positive/negative blocks only when the selected tool or workflow supports them. Verify exact syntax and model-specific controls before including them.

## Video, audio, 3D, and workflow tools

Examples include Sora, Runway, Kling, LTX Video, Dream Machine, ElevenLabs, Meshy, Tripo, Rodin, Blender or Unity assistants, Zapier, Make, and n8n.

- **Video:** Specify the subject's action, shot or camera movement, scene continuity, style, and duration or aspect ratio when known and supported.
- **Voice and audio:** Specify speaker, audience, language, tone, pacing, pronunciation, and emphasis. Use markup only if the target accepts it.
- **3D:** Specify the asset, style, silhouette, materials, intended use, and export or technical constraints when relevant. Ask for a reference or target model only when it changes the result.
- **Workflow automation:** Describe the trigger, conditions, actions, field mapping, and expected result. Identify connected services as assumptions; never include credentials.

## A target not listed here

Identify its closest interaction type from the sections above. If it is unclear whether the target creates content, edits a project, searches the web, or takes actions, ask one focused question. If exact platform syntax matters and cannot be verified, produce a portable prompt and mark that syntax as unverified rather than guessing.

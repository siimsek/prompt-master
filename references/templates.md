# Prompt Templates Reference

Full template library for Prompt Master. Read the relevant template when the user's task type matches. Do not load all templates at once — only the one you need.

## Table of Contents

| Template | Best For |
|----------|----------|
| [A — RTF](#template-a--rtf) | Simple one-shot tasks |
| [B — CO-STAR](#template-b--co-star) | Professional documents, business writing |
| [C — RISEN](#template-c--risen) | Complex multi-step projects |
| [D — CRISPE](#template-d--crispe) | Creative work, brand voice |
| [E — Auditable Reasoning](#template-e--auditable-reasoning) | Logic, math, analysis, debugging |
| [F — Few-Shot](#template-f--few-shot) | Consistent structured output, pattern replication |
| [G — File-Scope](#template-g--file-scope) | Cursor, Windsurf, Copilot — code editing AI |
| [H — Agent Task + Boundaries](#template-h--agent-task--boundaries) | Coding and autonomous agents |
| [I — Visual Descriptor](#template-i--visual-descriptor) | Midjourney, DALL-E, Stable Diffusion, Sora |
| [J — Reference Image Editing](#template-j--reference-image-editing) | Editing an existing image with a reference |
| [K — ComfyUI](#template-k--comfyui) | ComfyUI node-based image workflows |
| [L — Prompt Decompiler](#template-l--prompt-decompiler) | Breaking down, adapting, or splitting existing prompts |
| [M — Portable Agent Task Brief](#template-m--portable-agent-task-brief) | Complex, multi-step work for coding or autonomous agents |

---

## Template A — RTF

*Role, Task, Format. Use for fast one-shot tasks where the request is clear and simple.*

```
Role: [One sentence defining who the AI is]
Task: [Precise verb + what to produce]
Format: [Exact output format and length]
```

**Example:**
```
Role: You are a senior technical writer.
Task: Write a one-paragraph description of what a REST API is.
Format: Plain prose, 3 sentences maximum, no jargon, suitable for a non-technical audience.
```

---

## Template B — CO-STAR

*Context, Objective, Style, Tone, Audience, Response. Use for professional documents, business writing, reports, and marketing content where full context control matters.*

```
Context: [Background the AI needs to understand the situation]
Objective: [Exact goal — what success looks like]
Style: [Writing style: formal / conversational / technical / narrative]
Tone: [Emotional register: authoritative / empathetic / urgent / neutral]
Audience: [Who reads this — their knowledge level and expectations]
Response: [Format, length, and structure of the output]
```

**Example:**
```
Context: I am a founder pitching a B2B SaaS tool that automates expense reporting for mid-size companies.
Objective: Write a cold email that gets a reply from a CFO.
Style: Direct and conversational, not salesy.
Tone: Confident but not pushy.
Audience: CFO at a 200-person company, busy, skeptical of vendor emails.
Response: 5 sentences max. Subject line included. No bullet points.
```

---

## Template C — RISEN

*Role, Instructions, Steps, End Goal, Narrowing. Use for complex projects, multi-step tasks, and any output that requires a clear sequence of actions.*

```
Role: [Expert identity the AI should adopt]
Instructions: [Overall task in plain terms]
Steps:
  1. [First action]
  2. [Second action]
  3. [Continue as needed]
End Goal: [What the final output must achieve]
Narrowing: [Constraints, scope limits, what to exclude]
```

**Example:**
```
Role: You are a product manager with 10 years of experience in mobile apps.
Instructions: Write a product requirements document for a habit tracking feature.
Steps:
  1. Define the problem statement in one paragraph
  2. List user stories in the format "As a [user], I want [goal] so that [reason]"
  3. Define acceptance criteria for each story
  4. List out-of-scope items explicitly
End Goal: A PRD that an engineering team can begin sprint planning from immediately.
Narrowing: No technical implementation details. No wireframes. Under 600 words total.
```

---

## Template D — CRISPE

*Capacity, Role, Insight, Statement, Personality, Experiment. Use for creative work, brand voice writing, and any task where personality, tone, and iteration matter.*

```
Capacity: [What capability or expertise the AI should have]
Role: [Specific persona to adopt]
Insight: [Key background insight that shapes the response]
Statement: [The core task or question]
Personality: [Tone and style — witty / authoritative / casual / sharp]
Experiment: [Request variants or alternatives to explore]
```

**Example:**
```
Capacity: Expert copywriter specializing in SaaS product launches.
Role: Brand voice for a productivity tool aimed at developers.
Insight: Developers hate marketing speak and respond to honesty and specificity.
Statement: Write the hero headline and sub-headline for the landing page.
Personality: Sharp, dry, confident — no adjectives, no exclamation marks.
Experiment: Give 3 variants ranging from minimal to bold.
```

---

## Template E — Auditable Reasoning

*Use for logic-heavy tasks, math, debugging, and multi-factor analysis where the result must be checkable without requesting private reasoning.*

```
[Task statement]

Return:
1. Conclusion
2. Assumptions
3. Evidence or intermediate results needed to audit the conclusion
4. Verification checks performed
5. Remaining uncertainty, if any

Do not reveal hidden chain-of-thought or private reasoning. Keep the rationale concise and decision-relevant.
```

**When to use:**
- Debugging where the cause is not obvious
- Comparing technical approaches
- Math or calculation requiring verification
- Analysis where evidence and assumptions must be inspectable

**When NOT to use:**
- Simple tasks where the answer is clear
- Creative tasks where an audit trail adds noise

---

## Template F — Few-Shot

*Use when examples clarify a format or style better than more prose.*

```
[Task instruction]

Here are examples of the exact format needed:

<examples>
  <example>
    <input>[example input 1]</input>
    <output>[example output 1]</output>
  </example>
  <example>
    <input>[example input 2]</input>
    <output>[example output 2]</output>
  </example>
</examples>

Now apply this exact pattern to: [actual input]
```

**Rules:**
- Use a small number of relevant examples, including an edge case when useful.
- Examples must include edge cases, not just easy cases.
- Use clear delimiters around examples. Use XML only when it suits the target prompt.
- If you have been re-prompting for the same formatting correction twice, switch to few-shot instead of rewriting instructions.

---

## Template G — File-Scope

*Use for Cursor, Windsurf, GitHub Copilot, and any AI that edits code inside a codebase. The most common failure mode here is editing the wrong file or breaking existing logic — this template prevents both.*

```
File: [exact/path/to/file.ext]
Function/Component: [exact name]

Current Behavior:
[What this code does right now — be specific]

Desired Change:
[What it should do after the edit — be specific]

Scope:
Only modify [function / component / section].
Do NOT touch: [list everything to leave unchanged]

Constraints:
- Language/framework: [specify version]
- Do not add dependencies not in [package.json / requirements.txt]
- Preserve existing [type signatures / API contracts / variable names]

Done When:
[Exact condition that confirms the change worked correctly]
```

---

## Template H — Agent Task + Boundaries

*Use for coding or autonomous agents that can inspect or change a project. Include only the boundaries and checkpoints that matter to the user's task and the target's controls.*

```
Objective:
[Single, unambiguous goal in one sentence]

Starting State:
[Current file structure / codebase state / environment]

Target State:
[What should exist when the agent is done]

Allowed Actions:
- [Actions needed for the requested task]

Out of Scope:
- [Files, systems, or actions that must remain untouched]

Approval Boundaries:
Pause before [specific destructive, external, or consequential action that needs user approval].

Checkpoints:
Report progress at [useful checkpoint, if needed]. At the end, summarize changes and checks actually performed.
```

---

## Template I — Visual Descriptor

*Use for Midjourney, DALL-E 3, Stable Diffusion, Sora, Runway, and any image or video generation tool.*

```
Subject: [Main subject]
Action/Pose: [What the subject is doing, if relevant]
Setting: [Where the scene takes place, if relevant]
Style and mood: [Visual direction]
Lighting and color: [Only if they affect the result]
Composition: [Framing, viewpoint, or layout]
Aspect ratio: [If supported and known]
Avoid: [Unwanted elements, if the target supports negative instructions]
Reference: [Attached image or style reference, if applicable]
```

Use prose, weighted tokens, negative prompts, or parameter flags only when supported by the selected tool and generation mode. Verify exact syntax and settings before including them.

---

## Template J — Reference Image Editing

*Use when the user has an existing image they want to modify. Focus on the requested change and what should remain stable.*

**When the target needs an uploaded reference, remind the user:**
"Attach your reference image to [tool name] before sending this prompt."

Check that the selected surface supports image editing and the provided reference type. Do not assume an endpoint, mode, flag, or strength value; verify exact controls when they matter.

```
Reference image: [attached / URL]
What to keep exactly the same: [list everything that must not change]
What to change: [specific edit only — be precise]
How much to change: [subtle / moderate / significant]
Style consistency: maintain the exact style, lighting, and mood of the reference
Negative prompt: [what to avoid introducing]
```

**Example:**
```
Reference image: [attached portrait photo]
What to keep exactly the same: face, hair, clothing, background, lighting
What to change: head angle — rotate from facing left to facing straight forward
How much to change: subtle, preserve all facial features exactly
Style consistency: maintain photorealistic style, same lighting direction
Negative prompt: no new elements, no style changes, no background changes
```

---

## Template K — ComfyUI

*Use for ComfyUI workflows. Match the output to the user's graph and loaded model.*

Ask which checkpoint or workflow is in use only if it changes prompt syntax or settings. Keep positive and negative prompts separate only when the graph expects separate inputs.

```
POSITIVE PROMPT:
[subject, style, mood, lighting, composition, and other relevant details]

NEGATIVE PROMPT:
[what to exclude, only if the workflow uses a negative prompt]

CHECKPOINT / WORKFLOW: [if relevant]
SETTINGS: [only verified values requested by the user]
```

---

## Template L — Prompt Decompiler

*Use when the user pastes an existing prompt and wants to break it down, adapt it for a different tool, simplify it, or understand its structure. This is analysis and adaptation, not building from scratch.*

**Detect which Decompiler task is needed:**
- **Break down** — explain what each part of the prompt does
- **Adapt** — rewrite for a different tool while preserving intent
- **Simplify** — remove redundancy and tighten without losing meaning
- **Split** — divide a complex one-shot prompt into a cleaner sequence

**For Adapt tasks, identify or ask for:**
"What tool is the original prompt from, and what tool are you adapting it for?"

**Break down output format:**
```
Original prompt: [paste]

Structure analysis:
- Role/Identity: [what role is assigned and why]
- Task: [what action is being requested]
- Constraints: [what limits are set]
- Format: [what output shape is expected]
- Weaknesses: [what is missing or could cause wrong output]

Recommended fix: [rewritten version with gaps filled]
```

**Adapt output format:**
```
Original ([source tool]): [original prompt]

Adapted for [target tool]:
[rewritten prompt using target tool syntax and best practices]

Key changes made:
- [change 1 and why]
- [change 2 and why]
```

**Split output format:**
```
Original prompt: [paste]

This prompt is doing [N] things. Split into [N] sequential prompts:

Prompt 1 — [what it handles]:
[prompt block]

Prompt 2 — [what it handles]:
[prompt block]

Run these in order. Each output feeds the next.
```
---

## Template M — Portable Agent Task Brief

*Use for complex, multi-step, or agentic work in a coding or autonomous agent. Adapt sections to the target's actual interface and capabilities; omit fields that do not affect the task.*

```
## Objective
[What needs to be built, fixed, or produced — one clear sentence. Add WHY if it affects approach.]

## Context
[What exists now — relevant files, current behavior, stack already in place, what was tried and failed]

## Expected Result
[What done looks like — specific files changed, behavior produced, tests passing. Binary where possible.]

## Scope
- Work only in: [specific files and directories]
- Do NOT touch: [forbidden files — .env, package-lock.json, configs, anything outside scope]

## Constraints
- [Relevant stack, conventions, compatibility needs, or dependency boundaries]
- Make only changes needed for the requested outcome.

## Acceptance Criteria
- [ ] [Binary check 1]
- [ ] [Binary check 2]
- [ ] [Binary check 3]

## Approval Boundaries
- Proceed with the in-scope work described above.
- Stop before [specific consequential action, external write, destructive change, or unresolved user decision].

## Verification and Handoff
Run [relevant checks]. Report changed files, results, and anything not verified. Do not claim a check passed unless it was run.
```

**Optional session context** — include this only if the target supports it and the user has supplied relevant prior-session decisions:
```
## Session Strategy
[Pick one:]
- New session — unrelated to prior context, start fresh
- Continue — prior context still needed
- Delegate — use only [independent, sizeable workstream], with a bounded deliverable
- Compact first — compact around [decisions, constraints, and current state], then begin
```

**When to use:** The task is complex, multi-file, ambiguous, or agentic. Not needed for simple one-shot tasks.

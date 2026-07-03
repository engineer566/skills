---
name: real-user-research
description: Search the web for authentic user discussions about a topic and summarize real user opinions from comments, forums, GitHub issues, and Reddit. Focuses on lived experience, not official docs or marketing.
---

# Real User Research

Search the web for authentic user discussions about a topic and summarize real user opinions. This skill focuses on lived experience from comments, forums, GitHub issues, and Reddit — not official documentation, blog posts, or marketing content.

## When to Use This Skill

Use this skill when the user:

- Wants to know "what real users think" about a tool, workflow, or practice
- Asks for community consensus rather than official guidance
- Wants to compare options based on actual user experiences
- Is researching adoption patterns, pain points, or workarounds
- Says things like "how do people actually do X?", "what's the community saying?", "any real-world experience with Y?"

## What This Skill Does

1. Searches the web for discussions on the target topic
2. Identifies pages likely to contain authentic user voices (Reddit, GitHub Issues/Discussions, Hacker News, forums, Stack Exchange)
3. Extracts comments and filters out obvious marketing, AI-generated fluff, and official docs
4. Summarizes user opinions by theme with citations back to specific users/threads
5. Surfaces disagreements and minority views, not just consensus

## What This Skill Does NOT Do

- Replace official documentation
- Provide a definitive "correct" answer
- Trust single anecdotes as universal truth
- Read paywalled or login-required content unless explicitly authorized

## Workflow

### Step 1: Clarify the Research Question

Before searching, confirm with the user:

1. The exact topic or question they want answered
2. The relevant communities (e.g., Reddit, HN, GitHub, specific forums)
3. Any time window they care about (recent vs. all time)
4. Whether they want broad consensus or deep dive into a specific pain point

If the question is vague, ask once for clarification. Do not proceed with a vague query.

### Step 2: Search for Authentic Discussions

Run multiple targeted searches. Good query patterns:

- `"<topic>" experience review site:reddit.com`
- `"<topic>" workflow "how do you" site:reddit.com`
- `"<tool name>" pain points OR "doesn't work" OR workaround`
- `"<tool name>" site:news.ycombinator.com`
- `"<tool name>" OR "<alternative>" site:github.com/discussions`

Use Tavily Web Search with `search_depth: advanced` and `include_raw_content: true`.

### Step 3: Identify High-Value Pages

Prefer pages with:

- Multiple commenters
- Specific examples or screenshots
- Technical detail
- Disagreement or follow-up questions
- Recent activity (unless researching historical consensus)

Avoid:

- Landing pages and product homepages
- Listicles that just aggregate links
- Posts that are clearly AI-generated or astroturfed
- Content that is mostly quotes from official docs

### Step 4: Extract Comments

For each high-value page, extract the actual user comments. Use `tavily_extract` or `WebFetch` with a prompt like:

> Extract all user comments about [topic]. For each commenter, list their username, key claims, specific experiences, and any workarounds they mention. Ignore ads, official responses, and generic fluff.

If a thread is large, focus on:

- Top-level comments
- Replies that add new information
- Comments with specific numbers, tools, or repos

### Step 5: Filter and Synthesize

Group findings by theme. For each theme, include:

- **Claim**: What users are saying
- **Evidence**: Specific usernames and quotes or paraphrases
- **Prevalence**: Is this a common view or a minority opinion?
- **Sources**: Links to the threads

Explicitly call out:

- Contradictory opinions
- Unresolved questions
- Hype vs. lived experience gaps
- Selection bias (e.g., only power users post on HN)

### Step 6: Present the Report

Structure the final response as:

```markdown
## Research Question

## Key Themes

### 1. [Theme Name]
- **What users say**: ...
- **Representative quotes**: "..." — u/username, [source](link)
- **Prevalence**: Common / split / minority

### 2. [Theme Name]
...

## Disagreements / Open Questions

## Bottom Line

## Sources
- [Title](link)
- [Title](link)
```

## Output Rules

1. **Always cite the specific user**, not just the thread.
2. **Distinguish consensus from anecdote.** Use phrases like "common complaint," "minority view," "one user reported."
3. **Quote directly when possible.** Paraphrase only when the original is too long or unclear.
4. **Include contradictory views.** Do not flatten the discussion into a single conclusion.
5. **Acknowledge limitations.** Mention if search results were sparse, paywalled, or mostly marketing.
6. **Never pretend a marketing page is a user review.**

## Example Invoices

**User**: "What do real users say about managing multiple Claude Code skills?"

**Agent**:
1. Search queries:
   - `"claude code" skills management symlink organize site:reddit.com`
   - `"claude code" skills too many slow context limit`
   - `"claude code skills" site:news.ycombinator.com`
2. Extract top Reddit threads and GitHub issues
3. Synthesize themes: "less is more," "scar not resume," "symlink workarounds," "skill discovery limitations"
4. Present report with usernames and links

## Quality Checklist

Before finishing, verify:

- [ ] At least 3 distinct sources are cited
- [ ] Every major claim has a user citation
- [ ] Contradictory or skeptical views are included
- [ ] Marketing/official content is labeled as such
- [ ] The "bottom line" does not overstate the evidence

## Safety Notes

- Some communities may contain toxic or off-topic content. Extract only material relevant to the research question.
- Do not reproduce slurs, harassment, or personal attacks, even if they appear in source threads.
- If a source appears to be astroturfing or undisclosed advertising, note the suspicion rather than treating it as authentic user opinion.

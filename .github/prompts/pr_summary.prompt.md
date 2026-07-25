---
agent: agent
description: Generate a filled PR description for the current branch against main.
---

Generate a filled pull request description for the current branch.

## Steps

1. Get the current branch name and the list of commits and changed files compared to `main` using git tools.
2. Read `pull_request_template.md` from the `.github` folder.
3. Fill out only the **Summary** and **Changes** sections based on the actual changes:
   - Write a concise **Summary** (what changed and why, not how).
   - Fill out the **Changes** section with a brief bullet list of what changed. Reference filenames only where necessary. No links, no paths, no line numbers. Exclude changelog fragments under `doc/changelog.d/`.
4. Save the filled content as a markdown file in the root of the repo named `<branch-name>_pr_summary.md` containing only the **Summary** and **Changes** sections.
5. Output the same content as a single markdown block in the chat, ready to paste into a GitHub PR description.

Keep the description to 2-3 sentences maximum. Do not invent changes that are not in the diff.
---
name: blog
description: Publish a personal blog post to the site
argument-hint: "<slug>"
---

# /blog — Publish a personal blog post

Target slug is `$ARGUMENTS`. Required — used as the filename and URL path.

## 1. Check if the post already exists

Look for `site/src/content/blog/{SLUG}.md`.

If it exists, display the current frontmatter and ask: "Ce billet existe déjà. Tu veux l'éditer ou repartir de zéro ?"

## 2. Collect post content

Ask for the content if not already provided in the conversation. The user may:
- Paste raw text directly
- Reference a file path to read

## 3. Structure the post

From the raw content, produce a well-structured markdown post:

### Frontmatter

```yaml
---
title: "{Title — derived from the content or first sentence}"
date: {TODAY in YYYY-MM-DD}
description: "{1-2 sentence summary for cards and OG meta}"
themes: [{relevant themes from: IA, Data, Leadership, Architecture, Tech, Sécurité, DevOps}]
---
```

### Body rules

- Keep the author's voice and style intact — do NOT rewrite or polish
- Add `## ` headings to structure if the text is long (>5 paragraphs) and doesn't have them
- Use markdown formatting: `**bold**` for emphasis, `code` for technical terms, `> blockquote` for citations
- Separate the closing reference/inspiration note with `---` in italics
- The first paragraph serves as the lead (styled via `article-intro` CSS)

Present the structured post and ask for validation before writing.

## 4. Image prompt

Generate an image prompt for the blog post.

**The mascot bible is `minion/.claude/commands/generate.md` — read its "Image prompt" section and
follow it.** It is the single source of truth for Le Veilleur's appearance and staging, because
the daily pipeline executes it in production; a second copy here would drift from it silently.
The only differences for a blog post: illustrate the post's own theme rather than the day's
sources, and there is no source list to draw topics from.

Display the generated prompt and ask: "Tu veux que je génère l'image ou tu as déjà un fichier ?"

If the user provides a file:

```bash
just add-blog-image {SLUG} {FILE_PATH}
```

Add `image: {SLUG}.png` to the frontmatter.

If the user wants to generate the image themselves, display the prompt for copy-paste and move on.
They can add the image later with `just add-blog-image`.

## 5. Write to site

Write the final markdown to `site/src/content/blog/{SLUG}.md`.

## 6. Verify build

```bash
cd site && npm run build 2>&1 | tail -5
```

Confirm the build succeeds and the post is rendered.

## 7. Publish

Commit the post and its image on a branch, then open a PR. A push to `main` touching `site/**`
deploys straight to Pages, so a blog post lands the moment it merges.

```bash
git switch -c blog/{SLUG}
git add site/src/content/blog/{SLUG}.md site/public/images/{SLUG}.png
git commit -m "feat: add {SLUG} blog post"
git push -u origin blog/{SLUG} && gh pr create --fill
```

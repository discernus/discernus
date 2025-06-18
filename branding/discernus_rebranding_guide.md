# Discernus Rebranding Rollout Guide

## Overview
This guide outlines a conservative, staged approach for rebranding your project to "Discernus." The goal is to minimize disruption, maintain continuity for users and contributors, and ensure a smooth transition across all project assets.

---

## Why a Conservative Approach?
- **Minimizes risk:** Avoids breaking code, imports, or user workflows during the transition.
- **Maintains continuity:** Ensures existing users and contributors are not confused or disrupted.
- **Allows gradual migration:** Gives time to update documentation, code, and ecosystem components in a controlled way.
- **Builds community buy-in:** Transparent, stepwise communication helps everyone adjust to the new brand.

---

## Step-by-Step Rollout Plan

### 1. GitHub Organization and Repo Name
- **Action:**
  - Create or rename the main repository to `discernus` under the `discernus` GitHub organization.
  - Update the repo description and README to use the new name and tagline.
- **Why:** This is the public face of your project and the anchor for all future code, documentation, and community contributions.

### 2. README and Documentation
- Update the main `README.md` with the new branding, tagline, and elevator pitch.
- Add a "naming rationale" or "rebranding announcement" section if you have existing users or contributors.
- Update all major documentation files (CONTRIBUTING.md, CODE_OF_CONDUCT.md, docs/ folder) to reference "Discernus."

### 3. Website and Social Media
- Update any project website, landing page, or documentation site to use the new name, logo, and color scheme.
- Update social media profiles (Twitter/X, etc.) with the new branding and logo.

### 4. Internal Codebase (Gradual)
- Keep the internal Python package and module names as-is for now (e.g., `narrative_gravity`), to avoid breaking imports and workflows.
- Begin planning for a future migration to `discernus` as the package/module name, but only after the MVP is stable and the community is notified.

### 5. Communication
- Announce the rebrand to collaborators, mailing lists, and any existing user base.
- Use the new name in all new blog posts, papers, and presentations.

### 6. Ecosystem and Plugins
- For any new modules, plugins, or sub-projects, use the `discernus-` prefix (e.g., `discernus-mft`, `discernus-lab`).

---

## Summary Table

| Step                | What to Change First         | Why?                        |
|---------------------|-----------------------------|-----------------------------|
| 1. GitHub Org/Repo  | Repo/org name, description  | Most visible, least breakage|
| 2. README/Docs      | Branding, tagline, pitch    | Sets tone for all users     |
| 3. Website/Social   | Logos, color, messaging     | Public-facing, easy to update|
| 4. Codebase         | Gradual, after MVP          | Avoids breaking code/users  |
| 5. Communication    | Announce, explain rationale | Transparency, community buy-in|
| 6. Plugins/Ecosystem| Use new prefix for new work | Consistency, future-proof   |

---

## Next Steps
- Start with the GitHub repo/org rename and README update.
- Proceed through the steps above, communicating changes as you go.
- Use this guide as a checklist for a smooth, low-risk rebranding to Discernus. 
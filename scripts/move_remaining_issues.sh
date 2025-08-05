#!/bin/bash

# Feature Complete
for issue in 194 191 190 188; do
  gh issue edit $issue --milestone "Alpha Feature Complete"
done

# Quality & Hygiene
for issue in 292 249 198 197 196 173 172; do
  gh issue edit $issue --milestone "Alpha Quality & Hygiene"
done

# Remove old milestone from all issues
gh api -X PATCH /repos/discernus/discernus/milestones/11 -f state=closed
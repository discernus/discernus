#!/bin/bash

# Feature Complete
for issue in 259 277 273 252 251 282 283 284; do
  gh issue edit $issue --milestone "Alpha Feature Complete"
done

# Quality & Hygiene
for issue in 291 301 303 302 300; do
  gh issue edit $issue --milestone "Alpha Quality & Hygiene"
done
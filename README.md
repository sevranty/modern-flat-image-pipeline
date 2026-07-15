# Modern Flat Image Pipeline

A reference-to-image Agent Skill that transforms visual references into new Modern Flat illustrations through structured analysis, explicit scene contracts, controlled generation, visual QA, and targeted correction.

## Status

Early architecture and canonical-skill development. The runtime contract is not released yet.

## Pipeline

```text
reference input
-> reference analysis
-> semantic / identity / composition locks
-> scene brief
-> Modern Flat style contract
-> generation specification
-> pre-generation gate
-> image generation or edit
-> visual QA
-> targeted correction
-> final delivery
```

Development is tracked in Issues #1, #2, #3, #4, #5, #8, and #9. Public documentation and visual presentation are tracked separately in Issues #11 and #12.

# NEXUS-PRESENCE (SMPI-001) Development Folder

This folder contains the planning and documentation for integrating the NEXUS-PRESENCE agentic skill into the Hermes framework.

## Artifacts
- `STRATEGY.md`: Explains the What, Why, and How of this emergent integration.
- `CHECKLIST.md`: Step-by-step implementation tasks.
- `README.md`: This file.

## Integration Details
The core logic resides in `tools/nexus_presence_core.py` (data structures and metrics) and `tools/nexus_presence_cli.py` (the execution interface).
The actual Hermes skill definition is at `skills/social-media/nexus-presence/SKILL.md`.

## Lessons Learned
- Creating independent data layers (`~/.nexus_presence` or local test dirs) allows the agent to iteratively save state (HIM, CTM) without risking the core codebase.
- The Voice Drift calculation uses simple Euclidean distances for rhythm and hedging; in a production setting, this should leverage LLM-based semantic embeddings (cosine similarity).

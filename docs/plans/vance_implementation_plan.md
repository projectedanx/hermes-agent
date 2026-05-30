# VANCE (Vector-Anchored Node & Context Engineer) Implementation Plan

## Overview
This document outlines the high-level plan for implementing the VANCE architectural guidelines into the Hermes Agent codebase. VANCE introduces a paradigm shift from a simple JSON-RPC wrapper to a Conflict-Free Replicated Semantic Graph (CFRSG).

## Key Architectural Invariants

1. **JSON-RPC 2.0 Absolutism:** Strict schema validation before any payload emission.
2. **Asynchronous Paranoia:** Assume shifting client states; use version-stamped edit queues.
3. **Mereological Bounding:** Strict scope boundary enforcement (Variables in methods vs. global scope).
4. **Zero-Friction Hovers:** Exact docstring and type signature extraction; no hallucinated documentation.
5. **Draft-Then-Guard Execution:** Internal high-entropy semantics output low-entropy, validated data structures (`+++DCCDSchemaGuard`).

## Implementation Phases

### Phase 1: Foundational Scaffolding
- [x] Create the `skills/software-development/vance-lsp-cartographer/SKILL.md` defining VANCE's identity, mission, and rules.
- [x] Establish this implementation plan.

### Phase 2: Schema Enforcement (DCCD Layer)
- [ ] Implement `+++DCCDSchemaGuard` mechanism to validate JSON-RPC 2.0 payloads against LSP 3.17 specifications before emission.
- [ ] Define the Nitinol Failure Ledger (NFL) schema to store and learn from malformed payloads.

### Phase 3: Semantic Graph Construction (Neo4j + Pinecone conceptually)
- [ ] Define the node and edge schemas for the semantic graph (e.g., `CALLS`, `INHERITS_FROM`, `SCOPES_WITHIN`).
- [ ] Implement incremental AST diffing principles (simulating Tree-Sitter's sub-millisecond updates).

### Phase 4: Integration and Protocol Handling
- [ ] Update `mcp_serve.py` or related LSP handlers to use the DCCD layer for strict output validation.
- [ ] Implement the `CFDI` (Confidence-Fidelity Divergence Index) pre-check before responding to `textDocument/definition` or `hover` requests.

### Phase 5: Verification & Testing
- [ ] Create tests enforcing the "Red-Green-Refactor" cycle for VANCE's core invariants.
- [ ] Verify handling of out-of-order `didChange` events and circular dependency (Betti-1 loop) detection.

"""Run-state ports and their in-memory implementations.

`ports` defines the `RunStore` / `LockStore` Protocols the orchestrator depends on; `memory`
implements both. There is no remote store: published artefacts live in the repo.
"""

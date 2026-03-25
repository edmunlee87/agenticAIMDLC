---
name: Phase 1B Workflow SDK
overview: "Implement Phase 1B: all workflow state and orchestration primitives inside `workflowsdk` -- event-sourced state store, stage registry + routing engine, candidate/selection registry, session/recovery manager, and full lifecycle tests."
todos:
  - id: p1b-models
    content: "Write workflowsdk/models.py: WorkflowState, WorkflowEvent, StageRecord, CandidateVersion, VersionSelection, SessionRecord, CheckpointRecord"
    status: completed
  - id: p1b-state-store
    content: "Write workflowsdk/state_store.py: WorkflowStateStore (append events, replay to rebuild state)"
    status: completed
  - id: p1b-stage-routing
    content: Write workflowsdk/stage_registry.py (StageRegistryLoader, TransitionGuard) and workflowsdk/routing_engine.py (RoutingEngine with prerequisite enforcement)
    status: completed
  - id: p1b-candidate-selection
    content: Write workflowsdk/candidate.py (CandidateRegistry) and workflowsdk/selection.py (SelectionRegistry with mandatory audit)
    status: completed
  - id: p1b-session-recovery
    content: Write workflowsdk/session.py (SessionManager) and workflowsdk/recovery.py (RecoveryManager + CheckpointManager)
    status: completed
  - id: p1b-bootstrap-service
    content: Write workflowsdk/bootstrap.py and workflowsdk/service.py (WorkflowService facade)
    status: completed
  - id: p1b-tests
    content: Write tests/integration/test_phase1b_workflow.py covering all Phase 1B scenarios
    status: completed
isProject: false
---

# Phase 1B: Workflow SDK Implementation

## Scope

Everything lives in `[sdk/workflowsdk/src/workflowsdk/](sdk/workflowsdk/src/workflowsdk/)` unless noted.
The `workflowsdk` takes runtime dependencies on `registry_sdk`, `observabilitysdk`, and `auditsdk` from Phase 1A.

## Module Layout

```
workflowsdk/
  models.py          -- WorkflowState, WorkflowEvent, StageRecord, CandidateVersion, VersionSelection, SessionRecord, CheckpointRecord
  state_store.py     -- WorkflowStateStore (event-sourced, append-only events, rebuild via replay)
  stage_registry.py  -- StageRegistryLoader (loads stage_registry.yaml), TransitionGuard
  routing_engine.py  -- RoutingEngine (route_next from workflow_routes.yaml + prerequisite check from stage_preconditions.yaml)
  candidate.py       -- CandidateRegistry
  selection.py       -- SelectionRegistry
  session.py         -- SessionManager
  recovery.py        -- RecoveryManager, CheckpointManager
  bootstrap.py       -- bootstrap_project_workflow (wires registry_sdk + state_store + observability)
  service.py         -- WorkflowService (facade aggregating all sub-components)
  __init__.py
```

## Key Design Decisions

- **Event-sourced state**: `WorkflowState` is rebuilt by replaying `WorkflowEvent` entries. Every mutation appends an event; nothing is updated in-place.
- **Governance fields on every event**: `run_id`, `project_id`, `session_id`, `trace_id`, `actor`, `stage_name`, `policy_context` are first-class on `WorkflowEvent`.
- **TransitionGuard blocks**: invalid stage transition, review pending, selection missing, policy breach.
- **RoutingEngine reads YAML**: uses `StageConfigResolver`-style lookup against `workflow_routes.yaml` + `stage_preconditions.yaml`. Falls back to `"complete"` terminal state.
- **CandidateRegistry + SelectionRegistry**: candidates are immutable snapshots; selection requires an audit record. Multiple candidates with no selection → block downstream transitions.
- **SessionManager**: create/resume/suspend/close; each operation emits an observability event.
- **RecoveryManager**: 4 paths (retry, rerun, rollback, resume); all paths preserve audit chain; `CheckpointManager` stores serialised state snapshots.
- **WorkflowService**: single facade injected with the Phase 1A services; all public methods return `BaseResult`.

## pyproject.toml updates

`[sdk/workflowsdk/pyproject.toml](sdk/workflowsdk/pyproject.toml)` — add deps: `mdl-registry-sdk`, `mdl-observability-sdk`, `mdl-audit-sdk`, `mdl-artifact-sdk`.

## Tests

`tests/integration/test_phase1b_workflow.py` covering:

- Full lifecycle: bootstrap → transition → block (review pending) → resume
- Candidate create + select + block-without-select
- Session create → suspend → resume → failed-resume (corrupt checkpoint)
- Routing with unmet prerequisites
- TransitionGuard enforcement (each block reason)
- Event replay produces consistent state


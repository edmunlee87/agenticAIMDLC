# Agentic AI MDLC Framework

**Hybrid ADLC-SDLC Framework for Agentic AI Model Lifecycle Automation**

A governed agentic operating system for the model development lifecycle (MDLC). Deterministic SDKs perform calculations; skills orchestrate workflow and reasoning; humans decide at governance gates via HITL; append-only observability and audit form the system of record.

## Architecture

```
platform_contracts  <- shared schemas, enums, result contracts (no internal deps)
platform_core       <- runtime resolver, controllers, bridges, base classes
 ├── runtime/       <- config_models (Pydantic), config_loader, stage_config_resolver, resolver
 ├── schemas/       <- BaseModelBase, BaseResult, payload models, common fragments
 ├── services/      <- BaseService and derivatives
 ├── controllers/   <- BaseController, Session/Workflow/Review/Recovery controllers
 ├── bridges/       <- BaseBridge, agent_bridge, jupyter_bridge
 └── utils/         <- IDFactory, TimeProvider, ResultFactory, DependencyContainer
```

## Quick Start

```bash
# Install all SDKs in editable mode (requires uv)
uv sync

# Run tests
pytest tests/
```

## Phase Status

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Foundation, Contracts, Pydantic Config Pack | In Progress |
| 1A | Core Utility SDKs (config, registry, observability, audit, artifact) | Pending |
| 1B | Workflow Engine (workflowsdk) | Pending |
| 1C | HITL and Review (hitlsdk) | Pending |
| 1D | Policy and Governance (policysdk) | Pending |
| 1E | Runtime Resolver, Controllers, Bridges | Pending |
| 2 | UX, Validation, Flow Viz, RAG, Shared Analytics | Pending |
| 3 | Domain SDKs, Canvas, Data Prep, Scale | Pending |

## Guiding Principles

- **Governance-first**: Every state mutation, decision, and artifact is traceable to actor, timestamp, stage, and policy context.
- **Config-driven runtime**: Tool allowlists, governance gates, role capabilities, retry policies, stage routes are all YAML + Pydantic.
- **Deterministic SDKs**: SDKs do deterministic work; skills reason; humans decide at governance gates.
- **Domain-agnostic core**: Platform shell is fully functional before any domain SDK exists.
- **Audit-complete payloads**: All schemas carry trace_id, correlation_id, actor, policy_context as first-class fields.

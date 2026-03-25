# Skill: Evidence Gap Detector
**Skill ID:** `support.evidence_gap_detector`
**Version:** 1.0.0
**Layer:** Support

---

## Purpose
Identify missing or incomplete evidence artifacts before a review stage opens.
Surface gaps proactively so the model developer can resolve them before the reviewer is blocked.

---

## When to Invoke
Invoked by `ReviewOrchestratorSkill` before opening any HITL review.
Also useful as a pre-flight check before governance gate escalation.

---

## Detection Logic

For each artifact_type in `review_template.panel_a_evidence_types`:
1. Query `ArtifactService` for artifacts of that type for the current run.
2. If not found → `MISSING` gap.
3. If found but `is_audit_required=True` and artifact has no audit record → `AUDIT_MISSING` gap.
4. If artifact schema validation fails → `INVALID` gap.

---

## Output Format

```
Evidence Gap Report
-------------------
Stage: <stage_id>
Run: <run_id>

Required Evidence:
  [OK]      dataset_snapshot     -- SnapshotID: snap_abc123
  [OK]      dq_report            -- ArtifactID: art_xyz789
  [MISSING] coarse_classing_table -- NOT FOUND
  [AUDIT]   woe_iv_table         -- Artifact found but no audit record

Gaps Found: 2
  - coarse_classing_table: artifact not registered for this run.
    Action: Run coarse_classing stage and register the output artifact.
  - woe_iv_table: audit record missing.
    Action: Re-register artifact with audit=True flag.

Recommendation: Resolve all gaps before opening the review.
```

---

## Policy Interaction
If any artifact with `is_audit_required=True` is MISSING or AUDIT_MISSING:
- Block review opening.
- Return `ERR_MISSING_EVIDENCE` to the workflow orchestrator.

---

## Token Guidance
- Token Mode: `MINIMAL`.
- Output is short; injected as a mandatory section in review context packs.

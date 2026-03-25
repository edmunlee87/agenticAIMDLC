# Payload flow pack  
  
====================================================================  
END-TO-END PAYLOAD FLOW PACK  
FOR ENTERPRISE AGENTIC AI MODEL LIFECYCLE PLATFORM  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This reference shows end-to-end payload flow for three real governed  
workflow cases:  
  
1. Coarse classing review  
2. Validation conclusion  
3. Monitoring breach review  
  
Each case shows the sequence:  
  
A. runtime_context  
B. resolved_stack  
C. review_payload  
D. interaction_payload  
E. standard_response_envelope  
  
The objective is to demonstrate how the platform should pass state and  
decisions cleanly across:  
- runtime resolver  
- agent bridge  
- UI workspace  
- human interaction  
- deterministic SDK layer  
- workflow state update layer  
  
====================================================================  
CASE 1. COARSE CLASSING REVIEW  
====================================================================  
  
--------------------------------------------------------------------  
1A. runtime_context  
--------------------------------------------------------------------  
  
{  
  "schema_name": "runtime_context",  
  "schema_version": "1.0",  
  "project_id": "proj_scorecard_001",  
  "run_id": "run_scorecard_015",  
  "session_id": "sess_002",  
  "active_role": "developer",  
  "active_domain": "scorecard",  
  "workflow_mode": "development",  
  "stage_context": {  
    "active_stage": "coarse_classing_review",  
    "stage_class": "review",  
    "stage_sequence_no": 6  
  },  
  "validation_mode": false,  
  "annual_review_mode": false,  
  "remediation_mode": false,  
  "policy_mode": "standard",  
  "pending_review_type": "coarse_classing",  
  "ui_entry_point": "main_workspace",  
  "selected_candidate_version_id": null,  
  "candidate_versions_present": true,  
  "failure_state": false,  
  "last_error_code": null,  
  "active_overlays": [  
    "strict-governance-overlay"  
  ],  
  "current_refs": {  
    "review_id": "rev_cc_001",  
    "validation_run_id": null,  
    "model_id": "mdl_scorecard_001",  
    "dataset_id": "ds_train_001",  
    "artifact_ids": [  
      "art_fine_bins_001",  
      "art_binning_candidate_001",  
      "art_binning_candidate_002"  
    ]  
  },  
  "token_mode": "standard_mode"  
}  
  
--------------------------------------------------------------------  
1B. resolved_stack  
--------------------------------------------------------------------  
  
{  
  "schema_name": "resolved_stack",  
  "schema_version": "1.0",  
  "project_id": "proj_scorecard_001",  
  "run_id": "run_scorecard_015",  
  "session_id": "sess_002",  
  "resolved_skills": {  
    "base_skills": [  
      "platform-base-rules",  
      "model-lifecycle-orchestrator"  
    ],  
    "role_skill": "developer-agent",  
    "domain_skill": "scorecard-domain",  
    "stage_skill": "coarse-classing-review",  
    "overlay_skills": [  
      "strict-governance-overlay"  
    ],  
    "support_skills": [  
      "candidate-comparison-assistant"  
    ]  
  },  
  "sdk_allowlist": [  
    "scorecardsdk",  
    "evaluation_sdk",  
    "hitlsdk",  
    "workflowsdk",  
    "artifactsdk",  
    "observabilitysdk",  
    "auditsdk",  
    "reporting_sdk",  
    "jupyter_bridge",  
    "widgetsdk"  
  ],  
  "ui_contract": {  
    "ui_mode": "three_panel_review_workspace",  
    "interaction_mode": "edit_and_finalize",  
    "requires_human_action": true,  
    "display_sections": [  
      "proposal",  
      "evidence",  
      "structured_edit_workspace",  
      "status",  
      "actions"  
    ]  
  },  
  "response_contract": {  
    "expected_response_schema": "standard_response_envelope",  
    "mandatory_statuses": [  
      "preview_ready",  
      "finalized",  
      "invalid_needs_review"  
    ]  
  }  
}  
  
--------------------------------------------------------------------  
1C. review_payload  
--------------------------------------------------------------------  
  
{  
  "schema_name": "review_payload",  
  "schema_version": "1.0",  
  "project_id": "proj_scorecard_001",  
  "run_id": "run_scorecard_015",  
  "session_id": "sess_002",  
  "review_id": "rev_cc_001",  
  "stage_name": "coarse_classing_review",  
  "review_type": "coarse_classing",  
  "review_status": "under_review",  
  "title": "Coarse Classing Review – Utilization Ratio",  
  "decision_required": true,  
  "actor_context": {  
    "expected_role": "developer",  
    "current_actor_role": "developer"  
  },  
  "proposal_summary": {  
    "business_summary": "Candidate B has more balanced support and preserves business meaning better than Candidate A.",  
    "technical_summary": "Candidate B has one near-threshold support warning but stronger IV retention and cleaner WoE pattern.",  
    "recommendation": "Preview Candidate B with bins 2 and 3 merged, then finalize if support is acceptable."  
  },  
  "evidence": {  
    "key_metrics": [  
      {  
        "metric_name": "iv_retention",  
        "metric_value": 0.91,  
        "metric_unit": "ratio",  
        "status": "pass"  
      },  
      {  
        "metric_name": "support_breach_count",  
        "metric_value": 1,  
        "metric_unit": "count",  
        "status": "warning"  
      },  
      {  
        "metric_name": "monotonicity_flag",  
        "metric_value": 1,  
        "metric_unit": "flag",  
        "status": "pass"  
      }  
    ],  
    "warnings": [  
      {  
        "warning_code": "WARN_SUPPORT_NEAR_THRESHOLD",  
        "summary": "One proposed group remains near the minimum support threshold.",  
        "severity": "moderate",  
        "linked_refs": {  
          "artifact_ids": [  
            "art_binning_candidate_002"  
          ],  
          "metric_ids": []  
        }  
      }  
    ],  
    "artifact_refs": [  
      {  
        "artifact_id": "art_fine_bins_001",  
        "artifact_type": "fine_bin_table",  
        "artifact_name": "utilization_ratio_fine_bins",  
        "version": "v1",  
        "uri_or_path": "s3://risk/model/scorecard/fine_bins/utilization_ratio_v1.parquet"  
      },  
      {  
        "artifact_id": "art_binning_candidate_002",  
        "artifact_type": "binning_summary_table",  
        "artifact_name": "utilization_ratio_candidate_b",  
        "version": "v2",  
        "uri_or_path": "s3://risk/model/scorecard/binning/utilization_ratio_candidate_b_v2.parquet"  
      }  
    ],  
    "candidate_summaries": [  
      {  
        "candidate_version_id": "cand_bin_001",  
        "candidate_name": "candidate_a",  
        "candidate_type": "binning_version",  
        "summary_metrics": [  
          {  
            "metric_name": "iv_retention",  
            "metric_value": 0.88,  
            "metric_unit": "ratio",  
            "status": "pass"  
          }  
        ],  
        "warning_count": 2  
      },  
      {  
        "candidate_version_id": "cand_bin_002",  
        "candidate_name": "candidate_b",  
        "candidate_type": "binning_version",  
        "summary_metrics": [  
          {  
            "metric_name": "iv_retention",  
            "metric_value": 0.91,  
            "metric_unit": "ratio",  
            "status": "pass"  
          }  
        ],  
        "warning_count": 1  
      }  
    ]  
  },  
  "actions": {  
    "allowed_actions": [  
      "preview_changes",  
      "accept",  
      "accept_with_edits",  
      "reject_and_rerun",  
      "escalate"  
    ],  
    "default_action": "preview_changes"  
  },  
  "structured_edit_schema": {  
    "edit_type": "bin_group_edit",  
    "required_fields": [  
      "groups"  
    ]  
  },  
  "linked_refs": {  
    "decision_id": null,  
    "validation_run_id": null,  
    "candidate_version_ids": [  
      "cand_bin_001",  
      "cand_bin_002"  
    ]  
  },  
  "timestamps": {  
    "created_timestamp": "2026-03-17T09:00:00+08:00",  
    "due_timestamp": "2026-03-19T18:00:00+08:00"  
  }  
}  
  
--------------------------------------------------------------------  
1D. interaction_payload  
--------------------------------------------------------------------  
  
{  
  "schema_name": "interaction_payload",  
  "schema_version": "1.0",  
  "project_id": "proj_scorecard_001",  
  "run_id": "run_scorecard_015",  
  "session_id": "sess_002",  
  "interaction_id": "int_cc_001",  
  "review_id": "rev_cc_001",  
  "stage_name": "coarse_classing_review",  
  "interaction_type": "edit_and_finalize",  
  "action": "accept_with_edits",  
  "actor": {  
    "actor_id": "user_dev_001",  
    "actor_role": "developer",  
    "actor_type": "human"  
  },  
  "selected_candidate_version_id": "cand_bin_002",  
  "structured_edits": {  
    "groups": [  
      {"label": "Bin 1", "source_bins": [1]},  
      {"label": "Bin 2", "source_bins": [2, 3]},  
      {"label": "Bin 3", "source_bins": [4]},  
      {"label": "Missing", "source_bins": ["MISSING"]}  
    ]  
  },  
  "parameters": {  
    "rerun_strategy": null,  
    "comparison_mode": null  
  },  
  "user_comment": "Merged bins 2 and 3 to improve support while keeping business interpretability.",  
  "attachments": {  
    "artifact_ids": [],  
    "external_refs": []  
  },  
  "timestamp": "2026-03-17T10:30:00+08:00"  
}  
  
--------------------------------------------------------------------  
1E. standard_response_envelope  
--------------------------------------------------------------------  
  
{  
  "schema_name": "standard_response_envelope",  
  "schema_version": "1.0",  
  "status": "finalized",  
  "message": "Edited coarse bins accepted and finalized for downstream WoE/IV review.",  
  "project_id": "proj_scorecard_001",  
  "run_id": "run_scorecard_015",  
  "session_id": "sess_002",  
  "current_stage": "coarse_classing_review",  
  "next_stage": "woe_iv_review",  
  "required_human_action": false,  
  "interaction_state": "finalized",  
  "warnings": [  
    {  
      "warning_code": "WARN_SUPPORT_NEAR_THRESHOLD",  
      "summary": "One group remains close to the minimum support threshold but within accepted tolerance.",  
      "severity": "low",  
      "linked_refs": {  
        "artifact_ids": ["art_coarse_bins_003"],  
        "metric_ids": []  
      }  
    }  
  ],  
  "errors": [],  
  "artifacts_created": [  
    {  
      "artifact_id": "art_coarse_bins_003",  
      "artifact_type": "coarse_bin_definition",  
      "artifact_name": "utilization_ratio_coarse_bins_v3",  
      "version": "v3",  
      "uri_or_path": "s3://risk/model/scorecard/coarse_bins/utilization_ratio_v3.json"  
    }  
  ],  
  "candidate_versions_created": [],  
  "selected_candidate_version_id": "cand_bin_002",  
  "updated_metrics": [  
    {  
      "metric_name": "iv_after",  
      "metric_value": 0.171,  
      "metric_unit": "ratio",  
      "status": "pass"  
    },  
    {  
      "metric_name": "support_breach_count",  
      "metric_value": 0,  
      "metric_unit": "count",  
      "status": "pass"  
    }  
  ],  
  "review_created": null,  
  "validation_updates": {  
    "finding_ids": [],  
    "conclusion_id": null  
  },  
  "workflow_state_patch": {  
    "review_status": "finalized",  
    "current_stage_status": "finalized",  
    "selected_candidate_version_id": "cand_bin_002"  
  },  
  "audit_ref": "audit://run_scorecard_015/rev_cc_001",  
  "event_ref": "event://evt_cc_200",  
  "token_usage_hint": {  
    "mode": "standard_mode",  
    "recommended_next_context": "compact"  
  }  
}  
  
====================================================================  
CASE 2. VALIDATION CONCLUSION  
====================================================================  
  
--------------------------------------------------------------------  
2A. runtime_context  
--------------------------------------------------------------------  
  
{  
  "schema_name": "runtime_context",  
  "schema_version": "1.0",  
  "project_id": "proj_pd_002",  
  "run_id": "run_val_020",  
  "session_id": "sess_val_003",  
  "active_role": "validator",  
  "active_domain": "pd",  
  "workflow_mode": "validation",  
  "stage_context": {  
    "active_stage": "validation_conclusion",  
    "stage_class": "review",  
    "stage_sequence_no": 17  
  },  
  "validation_mode": true,  
  "annual_review_mode": false,  
  "remediation_mode": false,  
  "policy_mode": "strict",  
  "pending_review_type": "validation_conclusion",  
  "ui_entry_point": "main_workspace",  
  "selected_candidate_version_id": "cand_model_004",  
  "candidate_versions_present": false,  
  "failure_state": false,  
  "last_error_code": null,  
  "active_overlays": [  
    "validation-pack-overlay",  
    "strict-governance-overlay"  
  ],  
  "current_refs": {  
    "review_id": "rev_val_conc_001",  
    "validation_run_id": "val_run_020",  
    "model_id": "mdl_pd_010",  
    "dataset_id": "ds_pd_dev_010",  
    "artifact_ids": [  
      "art_val_findings_020",  
      "art_fitness_matrix_020",  
      "art_model_perf_020"  
    ]  
  },  
  "token_mode": "deep_review_mode"  
}  
  
--------------------------------------------------------------------  
2B. resolved_stack  
--------------------------------------------------------------------  
  
{  
  "schema_name": "resolved_stack",  
  "schema_version": "1.0",  
  "project_id": "proj_pd_002",  
  "run_id": "run_val_020",  
  "session_id": "sess_val_003",  
  "resolved_skills": {  
    "base_skills": [  
      "platform-base-rules",  
      "model-lifecycle-orchestrator"  
    ],  
    "role_skill": "validator-agent",  
    "domain_skill": "pd-domain",  
    "stage_skill": "validation-conclusion",  
    "overlay_skills": [  
      "validation-pack-overlay",  
      "strict-governance-overlay"  
    ],  
    "support_skills": [  
      "evidence-gap-detector",  
      "issue-severity-advisor"  
    ]  
  },  
  "sdk_allowlist": [  
    "validationsdk",  
    "hitlsdk",  
    "auditsdk",  
    "policysdk",  
    "reporting_sdk",  
    "workflowsdk",  
    "observabilitysdk",  
    "artifactsdk",  
    "knowledge_sdk",  
    "rag_sdk",  
    "jupyter_bridge",  
    "widgetsdk"  
  ],  
  "ui_contract": {  
    "ui_mode": "validation_review_workspace",  
    "interaction_mode": "review_and_conclude",  
    "requires_human_action": true,  
    "display_sections": [  
      "fitness_matrix",  
      "findings",  
      "conditions",  
      "conclusion_options",  
      "actions"  
    ]  
  },  
  "response_contract": {  
    "expected_response_schema": "standard_response_envelope",  
    "mandatory_statuses": [  
      "preview_ready",  
      "finalized",  
      "blocked"  
    ]  
  }  
}  
  
--------------------------------------------------------------------  
2C. review_payload  
--------------------------------------------------------------------  
  
{  
  "schema_name": "review_payload",  
  "schema_version": "1.0",  
  "project_id": "proj_pd_002",  
  "run_id": "run_val_020",  
  "session_id": "sess_val_003",  
  "review_id": "rev_val_conc_001",  
  "stage_name": "validation_conclusion",  
  "review_type": "validation_conclusion",  
  "review_status": "under_review",  
  "title": "Validation Conclusion Review – PD Model v10",  
  "decision_required": true,  
  "actor_context": {  
    "expected_role": "validator",  
    "current_actor_role": "validator"  
  },  
  "proposal_summary": {  
    "business_summary": "Model is usable with conditions. Core performance is acceptable, but evidence for one recalibration assumption remains limited.",  
    "technical_summary": "Calibration and discrimination are acceptable. Documentation and implementation evidence are complete. One methodology finding remains open but not sufficient to block use.",  
    "recommendation": "Conclude fit_for_use_with_conditions and require monthly monitoring of calibration drift for the first three periods."  
  },  
  "evidence": {  
    "key_metrics": [  
      {  
        "metric_name": "conceptual_soundness_status",  
        "metric_value": 1,  
        "metric_unit": "flag",  
        "status": "warning"  
      },  
      {  
        "metric_name": "calibration_status",  
        "metric_value": 1,  
        "metric_unit": "flag",  
        "status": "pass"  
      },  
      {  
        "metric_name": "implementation_readiness_status",  
        "metric_value": 1,  
        "metric_unit": "flag",  
        "status": "pass"  
      }  
    ],  
    "warnings": [  
      {  
        "warning_code": "WARN_LIMITED_EVIDENCE_RECALIBRATION",  
        "summary": "Evidence supporting one recalibration assumption is limited.",  
        "severity": "moderate",  
        "linked_refs": {  
          "artifact_ids": ["art_val_findings_020"],  
          "metric_ids": []  
        }  
      }  
    ],  
    "artifact_refs": [  
      {  
        "artifact_id": "art_val_findings_020",  
        "artifact_type": "validation_findings_summary",  
        "artifact_name": "validation_findings_pd_v10",  
        "version": "v1",  
        "uri_or_path": "s3://risk/validation/pd/v10/findings_summary.parquet"  
      },  
      {  
        "artifact_id": "art_fitness_matrix_020",  
        "artifact_type": "fitness_matrix",  
        "artifact_name": "fitness_matrix_pd_v10",  
        "version": "v1",  
        "uri_or_path": "s3://risk/validation/pd/v10/fitness_matrix.json"  
      }  
    ],  
    "candidate_summaries": []  
  },  
  "actions": {  
    "allowed_actions": [  
      "preview_changes",  
      "finalize_validation_conclusion",  
      "request_more_analysis",  
      "escalate"  
    ],  
    "default_action": "preview_changes"  
  },  
  "structured_edit_schema": {  
    "edit_type": "validation_conclusion_edit",  
    "required_fields": [  
      "conclusion_category"  
    ]  
  },  
  "linked_refs": {  
    "decision_id": null,  
    "validation_run_id": "val_run_020",  
    "candidate_version_ids": []  
  },  
  "timestamps": {  
    "created_timestamp": "2026-03-17T11:00:00+08:00",  
    "due_timestamp": "2026-03-20T18:00:00+08:00"  
  }  
}  
  
--------------------------------------------------------------------  
2D. interaction_payload  
--------------------------------------------------------------------  
  
{  
  "schema_name": "interaction_payload",  
  "schema_version": "1.0",  
  "project_id": "proj_pd_002",  
  "run_id": "run_val_020",  
  "session_id": "sess_val_003",  
  "interaction_id": "int_val_conc_001",  
  "review_id": "rev_val_conc_001",  
  "stage_name": "validation_conclusion",  
  "interaction_type": "review_and_conclude",  
  "action": "finalize_validation_conclusion",  
  "actor": {  
    "actor_id": "user_val_001",  
    "actor_role": "validator",  
    "actor_type": "human"  
  },  
  "selected_candidate_version_id": null,  
  "structured_edits": {  
    "conclusion_category": "fit_for_use_with_conditions",  
    "conditions": [  
      "Monitor calibration drift monthly for the first 3 production periods.",  
      "Document recalibration evidence expansion in the next annual review."  
    ]  
  },  
  "parameters": {  
    "rerun_strategy": null,  
    "comparison_mode": null  
  },  
  "user_comment": "Model is acceptable for use, but ongoing monitoring and documentation follow-up are required.",  
  "attachments": {  
    "artifact_ids": [],  
    "external_refs": []  
  },  
  "timestamp": "2026-03-17T12:15:00+08:00"  
}  
  
--------------------------------------------------------------------  
2E. standard_response_envelope  
--------------------------------------------------------------------  
  
{  
  "schema_name": "standard_response_envelope",  
  "schema_version": "1.0",  
  "status": "finalized",  
  "message": "Validation conclusion recorded as fit_for_use_with_conditions.",  
  "project_id": "proj_pd_002",  
  "run_id": "run_val_020",  
  "session_id": "sess_val_003",  
  "current_stage": "validation_conclusion",  
  "next_stage": "deployment_readiness",  
  "required_human_action": false,  
  "interaction_state": "finalized",  
  "warnings": [],  
  "errors": [],  
  "artifacts_created": [  
    {  
      "artifact_id": "art_val_conclusion_020",  
      "artifact_type": "validation_conclusion_note",  
      "artifact_name": "validation_conclusion_pd_v10",  
      "version": "v1",  
      "uri_or_path": "s3://risk/validation/pd/v10/conclusion_v1.docx"  
    }  
  ],  
  "candidate_versions_created": [],  
  "selected_candidate_version_id": null,  
  "updated_metrics": [],  
  "review_created": null,  
  "validation_updates": {  
    "finding_ids": [  
      "find_201",  
      "find_202"  
    ],  
    "conclusion_id": "vcon_020"  
  },  
  "workflow_state_patch": {  
    "validation_conclusion_status": "finalized",  
    "current_stage_status": "finalized"  
  },  
  "audit_ref": "audit://run_val_020/vcon_020",  
  "event_ref": "event://evt_val_450",  
  "token_usage_hint": {  
    "mode": "deep_review_mode",  
    "recommended_next_context": "compact"  
  }  
}  
  
====================================================================  
CASE 3. MONITORING BREACH REVIEW  
====================================================================  
  
--------------------------------------------------------------------  
3A. runtime_context  
--------------------------------------------------------------------  
  
{  
  "schema_name": "runtime_context",  
  "schema_version": "1.0",  
  "project_id": "proj_scorecard_live_001",  
  "run_id": "run_mon_030",  
  "session_id": "sess_mon_005",  
  "active_role": "monitoring",  
  "active_domain": "scorecard",  
  "workflow_mode": "monitoring",  
  "stage_context": {  
    "active_stage": "monitoring_breach_review",  
    "stage_class": "review",  
    "stage_sequence_no": 4  
  },  
  "validation_mode": false,  
  "annual_review_mode": false,  
  "remediation_mode": false,  
  "policy_mode": "strict",  
  "pending_review_type": "monitoring_breach",  
  "ui_entry_point": "main_workspace",  
  "selected_candidate_version_id": null,  
  "candidate_versions_present": false,  
  "failure_state": false,  
  "last_error_code": null,  
  "active_overlays": [  
    "strict-governance-overlay"  
  ],  
  "current_refs": {  
    "review_id": "rev_mon_010",  
    "validation_run_id": null,  
    "model_id": "mdl_scorecard_live_001",  
    "dataset_id": "ds_monitoring_2026_03",  
    "artifact_ids": [  
      "art_monitoring_kpi_202603",  
      "art_monitoring_breach_202603"  
    ]  
  },  
  "token_mode": "standard_mode"  
}  
  
--------------------------------------------------------------------  
3B. resolved_stack  
--------------------------------------------------------------------  
  
{  
  "schema_name": "resolved_stack",  
  "schema_version": "1.0",  
  "project_id": "proj_scorecard_live_001",  
  "run_id": "run_mon_030",  
  "session_id": "sess_mon_005",  
  "resolved_skills": {  
    "base_skills": [  
      "platform-base-rules",  
      "model-lifecycle-orchestrator"  
    ],  
    "role_skill": "monitoring-agent",  
    "domain_skill": "scorecard-domain",  
    "stage_skill": "monitoring-breach-review",  
    "overlay_skills": [  
      "strict-governance-overlay"  
    ],  
    "support_skills": [  
      "policy-breach-explainer"  
    ]  
  },  
  "sdk_allowlist": [  
    "monitoringsdk",  
    "policysdk",  
    "hitlsdk",  
    "auditsdk",  
    "reporting_sdk",  
    "workflowsdk",  
    "observabilitysdk",  
    "artifactsdk",  
    "knowledge_sdk",  
    "rag_sdk",  
    "jupyter_bridge",  
    "widgetsdk"  
  ],  
  "ui_contract": {  
    "ui_mode": "dashboard_review_workspace",  
    "interaction_mode": "triage_and_disposition",  
    "requires_human_action": true,  
    "display_sections": [  
      "current_snapshot_kpis",  
      "trend_view",  
      "breach_summary",  
      "segment_drilldown",  
      "actions"  
    ]  
  },  
  "response_contract": {  
    "expected_response_schema": "standard_response_envelope",  
    "mandatory_statuses": [  
      "finalized",  
      "escalated",  
      "blocked"  
    ]  
  }  
}  
  
--------------------------------------------------------------------  
3C. review_payload  
--------------------------------------------------------------------  
  
{  
  "schema_name": "review_payload",  
  "schema_version": "1.0",  
  "project_id": "proj_scorecard_live_001",  
  "run_id": "run_mon_030",  
  "session_id": "sess_mon_005",  
  "review_id": "rev_mon_010",  
  "stage_name": "monitoring_breach_review",  
  "review_type": "monitoring_breach",  
  "review_status": "under_review",  
  "title": "Monitoring Breach Review – March 2026 Snapshot",  
  "decision_required": true,  
  "actor_context": {  
    "expected_role": "monitoring",  
    "current_actor_role": "monitoring"  
  },  
  "proposal_summary": {  
    "business_summary": "The March 2026 snapshot shows severe score drift and moderate shift in portfolio composition.",  
    "technical_summary": "PSI for score distribution exceeded the severe threshold. The drift has persisted for two consecutive periods.",  
    "recommendation": "Escalate to remediation planning and assign root cause review."  
  },  
  "evidence": {  
    "key_metrics": [  
      {  
        "metric_name": "psi_score",  
        "metric_value": 0.31,  
        "metric_unit": "ratio",  
        "status": "breach"  
      },  
      {  
        "metric_name": "gini_change",  
        "metric_value": -0.04,  
        "metric_unit": "delta",  
        "status": "warning"  
      },  
      {  
        "metric_name": "segment_mix_shift",  
        "metric_value": 0.12,  
        "metric_unit": "ratio",  
        "status": "warning"  
      }  
    ],  
    "warnings": [  
      {  
        "warning_code": "WARN_SEVERE_SCORE_DRIFT",  
        "summary": "Score PSI exceeded severe threshold.",  
        "severity": "high",  
        "linked_refs": {  
          "artifact_ids": ["art_monitoring_breach_202603"],  
          "metric_ids": []  
        }  
      }  
    ],  
    "artifact_refs": [  
      {  
        "artifact_id": "art_monitoring_kpi_202603",  
        "artifact_type": "monitoring_kpi_table",  
        "artifact_name": "scorecard_monitoring_kpi_mar_2026",  
        "version": "v1",  
        "uri_or_path": "s3://risk/monitoring/scorecard/mar2026/kpi_table.parquet"  
      },  
      {  
        "artifact_id": "art_monitoring_breach_202603",  
        "artifact_type": "threshold_breach_table",  
        "artifact_name": "scorecard_breach_mar_2026",  
        "version": "v1",  
        "uri_or_path": "s3://risk/monitoring/scorecard/mar2026/breach_table.parquet"  
      }  
    ],  
    "candidate_summaries": []  
  },  
  "actions": {  
    "allowed_actions": [  
      "assign_remediation",  
      "approve_with_conditions",  
      "escalate",  
      "request_more_analysis"  
    ],  
    "default_action": "assign_remediation"  
  },  
  "structured_edit_schema": {  
    "edit_type": "monitoring_disposition_edit",  
    "required_fields": [  
      "action_class",  
      "owner_id",  
      "due_date"  
    ]  
  },  
  "linked_refs": {  
    "decision_id": null,  
    "validation_run_id": null,  
    "candidate_version_ids": []  
  },  
  "timestamps": {  
    "created_timestamp": "2026-03-17T13:00:00+08:00",  
    "due_timestamp": "2026-03-18T18:00:00+08:00"  
  }  
}  
  
--------------------------------------------------------------------  
3D. interaction_payload  
--------------------------------------------------------------------  
  
{  
  "schema_name": "interaction_payload",  
  "schema_version": "1.0",  
  "project_id": "proj_scorecard_live_001",  
  "run_id": "run_mon_030",  
  "session_id": "sess_mon_005",  
  "interaction_id": "int_mon_010",  
  "review_id": "rev_mon_010",  
  "stage_name": "monitoring_breach_review",  
  "interaction_type": "triage_and_disposition",  
  "action": "assign_remediation",  
  "actor": {  
    "actor_id": "user_mon_001",  
    "actor_role": "monitoring",  
    "actor_type": "human"  
  },  
  "selected_candidate_version_id": null,  
  "structured_edits": {  
    "action_class": "root_cause_review",  
    "owner_id": "user_risk_777",  
    "due_date": "2026-04-15",  
    "priority": "high"  
  },  
  "parameters": {  
    "rerun_strategy": null,  
    "comparison_mode": null  
  },  
  "user_comment": "Persistent severe score drift requires immediate root cause analysis and remediation tracking.",  
  "attachments": {  
    "artifact_ids": [],  
    "external_refs": []  
  },  
  "timestamp": "2026-03-17T13:45:00+08:00"  
}  
  
--------------------------------------------------------------------  
3E. standard_response_envelope  
--------------------------------------------------------------------  
  
{  
  "schema_name": "standard_response_envelope",  
  "schema_version": "1.0",  
  "status": "escalated",  
  "message": "Monitoring breach disposition recorded and remediation planning has been triggered.",  
  "project_id": "proj_scorecard_live_001",  
  "run_id": "run_mon_030",  
  "session_id": "sess_mon_005",  
  "current_stage": "monitoring_breach_review",  
  "next_stage": "remediation_planning",  
  "required_human_action": true,  
  "interaction_state": "escalated",  
  "warnings": [  
    {  
      "warning_code": "WARN_SEVERE_SCORE_DRIFT",  
      "summary": "Persistent severe score drift remains unresolved.",  
      "severity": "high",  
      "linked_refs": {  
        "artifact_ids": ["art_monitoring_breach_202603"],  
        "metric_ids": []  
      }  
    }  
  ],  
  "errors": [],  
  "artifacts_created": [],  
  "candidate_versions_created": [],  
  "selected_candidate_version_id": null,  
  "updated_metrics": [  
    {  
      "metric_name": "psi_score",  
      "metric_value": 0.31,  
      "metric_unit": "ratio",  
      "status": "breach"  
    }  
  ],  
  "review_created": {  
    "review_id": "rev_rem_001",  
    "review_type": "remediation_planning",  
    "review_status": "pending_review"  
  },  
  "validation_updates": {  
    "finding_ids": [],  
    "conclusion_id": null  
  },  
  "workflow_state_patch": {  
    "current_stage_status": "escalated",  
    "remediation_mode": true  
  },  
  "audit_ref": "audit://run_mon_030/breach_010",  
  "event_ref": "event://evt_mon_510",  
  "token_usage_hint": {  
    "mode": "standard_mode",  
    "recommended_next_context": "compact"  
  }  
}  
  
====================================================================  
4. FLOW SUMMARY OF THE 3 CASES  
====================================================================  
  
4.1 Coarse Classing Review  
--------------------------------------------------------------------  
runtime_context  
-> resolved_stack  
-> review_payload  
-> human edits bins in workspace  
-> interaction_payload  
-> scorecardsdk + evaluation_sdk validate and recompute  
-> standard_response_envelope finalized  
-> workflow moves to woe_iv_review  
  
4.2 Validation Conclusion  
--------------------------------------------------------------------  
runtime_context  
-> resolved_stack  
-> review_payload  
-> validator chooses conclusion category and conditions  
-> interaction_payload  
-> validationsdk + policysdk + auditsdk finalize  
-> standard_response_envelope finalized  
-> workflow moves to deployment_readiness  
  
4.3 Monitoring Breach Review  
--------------------------------------------------------------------  
runtime_context  
-> resolved_stack  
-> review_payload  
-> monitoring user assigns remediation  
-> interaction_payload  
-> monitoringsdk + policysdk + workflowsdk escalate  
-> standard_response_envelope escalated  
-> workflow moves to remediation_planning  
  
====================================================================  
5. DESIGN NOTES  
====================================================================  
  
5.1 Same Contract, Different Context  
--------------------------------------------------------------------  
All three cases use the same schema pack, but with different:  
- role  
- domain  
- stage  
- interaction mode  
- SDK allowlist  
- UI mode  
  
5.2 Deterministic and Governed  
--------------------------------------------------------------------  
The examples show that:  
- state is explicit  
- stage behavior is explicit  
- human action is explicit  
- final status is explicit  
- audit and event refs are explicit  
  
5.3 Token Thrift  
--------------------------------------------------------------------  
The objects are compact enough for orchestration and UI integration,  
while large evidence remains in artifacts referenced by ID/path.  
  
====================================================================  
END OF END-TO-END PAYLOAD FLOW PACK  
====================================================================  

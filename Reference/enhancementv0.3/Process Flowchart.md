# Process Flowchart  
  
flowchart TD  
    %% =========================================================  
    %% MASTER CONCEPT DIAGRAM  
    %% CREDIT SCORING AGENTIC AI WORKSPACE  
    %% CONTRACT + WORKFLOW + ORCHESTRATION + RESOLVERS + HITL  
    %% =========================================================  
  
    %% ---------------------------------------------------------  
    %% USER + FRONTEND ENTRY  
    %% ---------------------------------------------------------  
    U0[User<br/>Developer / Validator / Monitoring / Governance / Approver]  
    U0 --> U1[Open JupyterLab Governed Workspace]  
    U1 --> U2[Choose:<br/>Resume prior project/run/review<br/>or start new project]  
    U2 --> U3[Workspace boot request]  
  
    %% ---------------------------------------------------------  
    %% FRONTEND WORKSPACE  
    %% ---------------------------------------------------------  
    subgraph FE[Frontend Workspace Layer - JupyterLab Main Area]  
        FE0[Workspace Shell<br/>Header + 3-panel layout + optional bottom/detail]  
        FE1[Left Panel<br/>Navigation / Candidates / Sections / Filters / Flow Nodes]  
        FE2[Center Panel<br/>Proposal / Preview / Evidence / Charts / Tables / Diff]  
        FE3[Right Panel<br/>Actions / Comments / Structured Edits / Rerun Params]  
        FE4[Bottom Panel<br/>Trace / Raw Detail / Audit Drilldown / Logs]  
        FE5[Chat Support Panel<br/>Advisory only]  
        FE6[Workspace Store<br/>authoritative frontend state cache]  
        FE7[Draft Store<br/>comment / edits / filters / rerun params]  
        FE8[Event Dispatcher]  
        FE9[Patch Merger]  
        FE10[Bridge Client]  
        FE11[Renderer Registry<br/>Review / Dashboard / Flow / Mixed / Wizard]  
        FE12[Local Validation<br/>required comment / schema shape / selection checks]  
        FE13[Loading / Error / Blocked / Sync banners]  
    end  
  
    U3 --> FE0  
    FE0 --> FE1  
    FE0 --> FE2  
    FE0 --> FE3  
    FE0 --> FE4  
    FE0 --> FE5  
    FE0 --> FE6  
    FE0 --> FE7  
    FE1 --> FE8  
    FE2 --> FE8  
    FE3 --> FE8  
    FE4 --> FE8  
    FE5 --> FE8  
    FE8 --> FE12  
    FE12 --> FE10  
    FE10 --> FE9  
    FE9 --> FE6  
    FE11 --> FE2  
    FE11 --> FE3  
    FE13 --> FE0  
  
    %% ---------------------------------------------------------  
    %% FRONTEND EVENT CONTRACT  
    %% ---------------------------------------------------------  
    subgraph EC[Frontend Event Contract]  
        EC1[Widget Event Envelope<br/>event_id<br/>event_type<br/>workspace_id<br/>panel_id<br/>actor<br/>payload<br/>client_ts<br/>client_meta]  
        EC2[Key Event Types<br/>LOAD_WORKSPACE<br/>REFRESH_WORKSPACE<br/>OPEN_REVIEW<br/>SELECT_CANDIDATE<br/>SELECT_NODE<br/>PREVIEW_EDIT<br/>SUBMIT_ACTION<br/>REQUEST_ROUTE<br/>OPEN_DETAIL]  
        EC3[Response Types<br/>FULL_WORKSPACE<br/>WORKSPACE_PATCH<br/>VALIDATION_RESULT<br/>NOTIFICATION<br/>REFRESH_REQUIRED]  
        EC4[Patch Contract<br/>runtime_decision_patch<br/>allowed_actions_patch<br/>panel_patches<br/>draft_state_patch<br/>refresh_token]  
    end  
  
    FE8 --> EC1  
    EC1 --> EC2  
    FE10 --> EC3  
    EC3 --> EC4  
    EC4 --> FE9  
  
    %% ---------------------------------------------------------  
    %% JUPYTER BRIDGE  
    %% ---------------------------------------------------------  
    subgraph JB[Jupyter Bridge Layer]  
        JB1[Jupyter Bridge]  
        JB2[Workspace State Store]  
        JB3[Event Router]  
        JB4[Payload Mapper]  
        JB5[Review Payload Mapper]  
        JB6[Dashboard Payload Mapper]  
        JB7[Flow Payload Mapper]  
        JB8[Workspace Builder]  
        JB9[Workspace Ref<br/>workspace_id / project_id / run_id / review_id / session_id]  
    end  
  
    FE10 --> JB1  
    JB1 --> JB2  
    JB1 --> JB3  
    JB1 --> JB4  
    JB4 --> JB5  
    JB4 --> JB6  
    JB4 --> JB7  
    JB1 --> JB8  
    JB8 --> JB9  
  
    %% ---------------------------------------------------------  
    %% RUNTIME RESOLUTION  
    %% ---------------------------------------------------------  
    subgraph RT[Runtime Resolution Layer]  
        RT1[Runtime Resolver]  
        RT2[Stage Config Resolver]  
        RT3[Role Config Resolver]  
        RT4[Tool Group Resolver]  
        RT5[Governance Rule Resolver]  
        RT6[Retry Policy Resolver]  
        RT7[Allowlist Resolver]  
        RT8[Precondition Checker]  
        RT9[UI Mode Resolver]  
        RT10[Interaction Mode Resolver]  
        RT11[Token Mode Resolver]  
        RT12[Resolved Runtime Decision<br/>stage_name<br/>actor_role<br/>access_mode<br/>allowed_tools<br/>blocked_tools<br/>review_required<br/>approval_required<br/>audit_required<br/>auto_continue_allowed<br/>recommended_ui_mode<br/>recommended_interaction_mode<br/>recommended_token_mode<br/>recommended_next_routes]  
    end  
  
    JB3 --> RT1  
    RT1 --> RT2  
    RT1 --> RT3  
    RT1 --> RT4  
    RT1 --> RT5  
    RT1 --> RT6  
    RT1 --> RT7  
    RT1 --> RT8  
    RT1 --> RT9  
    RT1 --> RT10  
    RT1 --> RT11  
    RT2 --> RT12  
    RT3 --> RT12  
    RT4 --> RT12  
    RT5 --> RT12  
    RT6 --> RT12  
    RT7 --> RT12  
    RT8 --> RT12  
    RT9 --> RT12  
    RT10 --> RT12  
    RT11 --> RT12  
  
    %% ---------------------------------------------------------  
    %% CONFIG / POLICY / STAGE REGISTRY  
    %% ---------------------------------------------------------  
    subgraph CFG[Config and Governance Registry]  
        CFG1[Runtime Master Config]  
        CFG2[Stage Registry]  
        CFG3[Stage Tool Matrix]  
        CFG4[Stage Preconditions]  
        CFG5[Role Capabilities]  
        CFG6[Tool Groups / Virtual Tool Groups]  
        CFG7[Governance Overlays]  
        CFG8[Retry Policies]  
        CFG9[Workflow Routes]  
        CFG10[Failure Routes]  
        CFG11[Domain Overlay - Scorecard / PD / LGD / EAD / SICR / ECL / Stress]  
        CFG12[Role Overlay - Developer / Validator / Monitoring / Governance / Approver / System]  
        CFG13[Environment Overlay - Dev / UAT / Prod]  
    end  
  
    CFG1 --> RT2  
    CFG2 --> RT2  
    CFG3 --> RT7  
    CFG4 --> RT8  
    CFG5 --> RT3  
    CFG6 --> RT4  
    CFG7 --> RT5  
    CFG8 --> RT6  
    CFG9 --> RT1  
    CFG10 --> RT1  
    CFG11 --> RT2  
    CFG11 --> RT7  
    CFG12 --> RT3  
    CFG12 --> RT7  
    CFG13 --> RT5  
    CFG13 --> RT6  
  
    %% ---------------------------------------------------------  
    %% CONTROLLERS  
    %% ---------------------------------------------------------  
    subgraph CT[Controller Orchestration Layer]  
        CT1[Session Controller]  
        CT2[Workflow Controller]  
        CT3[Review Controller]  
        CT4[DataPrep Controller]  
        CT5[Validation Controller]  
        CT6[Monitoring Controller]  
        CT7[Controller Factory]  
        CT8[Base Controller<br/>runtime checks + tool allowance + response envelope + workflow patch + audit + observability]  
    end  
  
    RT12 --> CT8  
    JB3 --> CT7  
    CT7 --> CT1  
    CT7 --> CT2  
    CT7 --> CT3  
    CT7 --> CT4  
    CT7 --> CT5  
    CT7 --> CT6  
    CT1 --> CT8  
    CT2 --> CT8  
    CT3 --> CT8  
    CT4 --> CT8  
    CT5 --> CT8  
    CT6 --> CT8  
  
    %% ---------------------------------------------------------  
    %% SHARED RESPONSE ENVELOPE  
    %% ---------------------------------------------------------  
    subgraph RC[Controller / Tool Response Contract]  
        RC1[Standard Result Envelope<br/>status<br/>message<br/>controller_name / action_name<br/>data<br/>warnings / errors<br/>references<br/>runtime_decision<br/>workflow_patch<br/>agent_hint<br/>audit_hint<br/>observability_hint]  
        RC2[Agent Hint<br/>reasoning_summary<br/>recommended_next_action<br/>requires_human_review<br/>suggested_followup_functions<br/>safe_to_continue]  
        RC3[Workflow Hint / Patch<br/>recommended_next_stage<br/>state_patch<br/>should_open_review<br/>review_type]  
        RC4[Audit Hint<br/>should_write_audit<br/>audit_type]  
        RC5[Observability Hint<br/>should_write_event<br/>event_type]  
    end  
  
    CT8 --> RC1  
    RC1 --> RC2  
    RC1 --> RC3  
    RC1 --> RC4  
    RC1 --> RC5  
    RC1 --> JB4  
    JB4 --> FE10  
  
    %% ---------------------------------------------------------  
    %% SDK / SERVICES  
    %% ---------------------------------------------------------  
    subgraph SDK[SDK and Service Layer]  
        S0[Registry Service]  
        S1[Workflow Service]  
        S2[HITL Service]  
        S3[DataPrep Service]  
        S4[Spark DataPrep Service]  
        S5[Dataset Service]  
        S6[Feature / Evaluation Service]  
        S7[Scorecard Service]  
        S8[Validation Service]  
        S9[Monitoring Service]  
        S10[Reporting Service]  
        S11[Knowledge Service]  
        S12[RAG / Retrieval Service]  
        S13[Flow Visualization Service]  
        S14[Observability Service]  
        S15[Audit Service]  
        S16[Policy Service]  
    end  
  
    CT1 --> S0  
    CT2 --> S1  
    CT2 --> S16  
    CT3 --> S2  
    CT4 --> S3  
    CT4 --> S4  
    CT4 --> S5  
    CT5 --> S8  
    CT5 --> S10  
    CT6 --> S9  
    CT6 --> S10  
    CT2 --> S11  
    CT2 --> S12  
    CT2 --> S13  
    CT8 --> S14  
    CT8 --> S15  
  
    %% ---------------------------------------------------------  
    %% DATA / ARTIFACT / KNOWLEDGE REGISTRIES  
    %% ---------------------------------------------------------  
    subgraph RG[Persistent State and Registry Layer]  
        RG1[Project Registry]  
        RG2[Run Registry]  
        RG3[Workflow State Store]  
        RG4[Review Registry]  
        RG5[Dataset Registry]  
        RG6[Dataset Snapshot Registry]  
        RG7[Candidate Version Registry]  
        RG8[Artifact Registry]  
        RG9[Validation Registry]  
        RG10[Monitoring Snapshot Registry]  
        RG11[Knowledge Registry]  
        RG12[Audit Store]  
        RG13[Observability Event Store]  
        RG14[Flow Graph / Timeline Store]  
    end  
  
    S0 --> RG1  
    S0 --> RG2  
    S1 --> RG3  
    S2 --> RG4  
    S5 --> RG5  
    S5 --> RG6  
    S7 --> RG7  
    S10 --> RG8  
    S8 --> RG9  
    S9 --> RG10  
    S11 --> RG11  
    S15 --> RG12  
    S14 --> RG13  
    S13 --> RG14  
  
    %% ---------------------------------------------------------  
    %% CREDIT SCORING DOMAIN WORKFLOW  
    %% ---------------------------------------------------------  
    subgraph WF[Credit Scoring Workflow Stages]  
        W1[Session Bootstrap]  
        W2[Workflow Bootstrap / Resume Selection]  
        W3[Data Preparation Config]  
        W4[Data Preparation Execution]  
        W5[Data Readiness Check]  
        W6[Dataset Registration + Snapshot]  
        W7[Feature Engineering]  
        W8[Fine Classing]  
        W9[Coarse Classing Candidate Build]  
        W10[Coarse Classing Review]  
        W11[WOE / IV Analysis]  
        W12[Feature Shortlist Build]  
        W13[Feature Shortlist Review]  
        W14[Model Fit Candidates]  
        W15[Metrics + Diagnostics + Comparison]  
        W16[Model Selection Review]  
        W17[Score Scaling + Banding]  
        W18[Scorecard Output Bundle]  
        W19[Validation Scope Init]  
        W20[Validation Evidence Intake]  
        W21[Methodology Review]  
        W22[Data Validation Review]  
        W23[Fitness Review]  
        W24[Validation Conclusion Review]  
        W25[Technical Reporting]  
        W26[Committee Pack Build]  
        W27[Approval / Signoff]  
        W28[Production Monitoring Setup]  
        W29[Monitoring Snapshot Ingest]  
        W30[Monitoring KPI Refresh]  
        W31[Monitoring Breach Review]  
        W32[Annual Review Build]  
        W33[Workflow Closed]  
    end  
  
    W1 --> W2  
    W2 --> W3  
    W3 --> W4  
    W4 --> W5  
    W5 --> W6  
    W6 --> W7  
    W7 --> W8  
    W8 --> W9  
    W9 --> W10  
    W10 --> W11  
    W11 --> W12  
    W12 --> W13  
    W13 --> W14  
    W14 --> W15  
    W15 --> W16  
    W16 --> W17  
    W17 --> W18  
    W18 --> W19  
    W19 --> W20  
    W20 --> W21  
    W21 --> W22  
    W22 --> W23  
    W23 --> W24  
    W24 --> W25  
    W25 --> W26  
    W26 --> W27  
    W27 --> W28  
    W28 --> W29  
    W29 --> W30  
    W30 --> W31  
    W31 --> W32  
    W32 --> W33  
  
    %% ---------------------------------------------------------  
    %% SDK MAPPING TO DOMAIN STAGES  
    %% ---------------------------------------------------------  
    W3 --> S3  
    W4 --> S4  
    W5 --> S4  
    W6 --> S5  
    W7 --> S6  
    W8 --> S7  
    W9 --> S7  
    W10 --> S2  
    W10 --> S7  
    W11 --> S7  
    W12 --> S7  
    W13 --> S2  
    W14 --> S7  
    W15 --> S6  
    W16 --> S2  
    W16 --> S1  
    W17 --> S7  
    W18 --> S10  
    W19 --> S8  
    W20 --> S8  
    W21 --> S8  
    W22 --> S8  
    W23 --> S8  
    W24 --> S2  
    W24 --> S8  
    W25 --> S10  
    W26 --> S10  
    W27 --> S2  
    W28 --> S9  
    W29 --> S9  
    W30 --> S9  
    W31 --> S2  
    W31 --> S9  
    W32 --> S9  
    W32 --> S10  
  
    %% ---------------------------------------------------------  
    %% HITL LOOP  
    %% ---------------------------------------------------------  
    subgraph HITL[Governed HITL Loop]  
        H1[Agent / Service generates proposal<br/>candidate / preview / conclusion option / breach view]  
        H2[Review Payload Builder]  
        H3[Render review workspace contract]  
        H4[Human selects candidate / section / node]  
        H5[Human previews edits]  
        H6[Human comments]  
        H7[Human approves / approves with conditions / rejects / escalates / reruns]  
        H8[Action validation]  
        H9[Decision capture]  
        H10[Workflow patch]  
        H11[Audit write]  
        H12[Observability event]  
        H13[Refresh workspace]  
    end  
  
    H1 --> H2  
    H2 --> H3  
    H3 --> H4  
    H4 --> H5  
    H4 --> H6  
    H5 --> H7  
    H6 --> H7  
    H7 --> H8  
    H8 --> H9  
    H9 --> H10  
    H9 --> H11  
    H9 --> H12  
    H10 --> H13  
  
    W10 --> H1  
    W13 --> H1  
    W16 --> H1  
    W24 --> H1  
    W31 --> H1  
  
    %% ---------------------------------------------------------  
    %% REVIEW / APPROVAL GATING  
    %% ---------------------------------------------------------  
    subgraph GV[Governance Gates]  
        G1{Review required?}  
        G2{Approval required?}  
        G3{Audit required?}  
        G4{Tool allowed by role, stage, policy, state?}  
        G5{Preconditions satisfied?}  
        G6{Severe breach / stale state / missing active review?}  
    end  
  
    RT12 --> G1  
    RT12 --> G2  
    RT12 --> G3  
    RT12 --> G4  
    RT12 --> G5  
    RT12 --> G6  
  
    G5 -->|No| FE13  
    G4 -->|No| FE13  
    G6 -->|Yes| FE13  
    G1 -->|Yes| H2  
    G2 -->|Yes| H7  
    G3 -->|Yes| H11  
  
    %% ---------------------------------------------------------  
    %% REVIEW AND FINALIZATION DECISIONS  
    %% ---------------------------------------------------------  
    D1{Data acceptable?}  
    D2{Coarse classing approved?}  
    D3{Feature shortlist approved?}  
    D4{Model selected?}  
    D5{Validation fit for use?}  
    D6{Monitoring breach resolved?}  
  
    W5 --> D1  
    D1 -->|No| W3  
    D1 -->|Yes| W6  
  
    W10 --> D2  
    D2 -->|No| W9  
    D2 -->|Yes| W11  
  
    W13 --> D3  
    D3 -->|No| W12  
    D3 -->|Yes| W14  
  
    W16 --> D4  
    D4 -->|No| W14  
    D4 -->|Yes| W17  
  
    W24 --> D5  
    D5 -->|No| W3  
    D5 -->|Yes| W25  
  
    W31 --> D6  
    D6 -->|No| W29  
    D6 -->|Yes| W32  
  
    %% ---------------------------------------------------------  
    %% KNOWLEDGE / RAG / FLOW  
    %% ---------------------------------------------------------  
    subgraph KF[Knowledge, Retrieval, and Flow]  
        K1[Capture knowledge from event]  
        K2[Capture knowledge from decision]  
        K3[Search knowledge]  
        K4[Retrieve compact context pack]  
        K5[Build flow nodes]  
        K6[Build flow edges]  
        K7[Build flow timeline]  
        K8[Build drilldown payload]  
        K9[Promote reusable knowledge]  
    end  
  
    S11 --> K1  
    S11 --> K2  
    S11 --> K3  
    S12 --> K4  
    S13 --> K5  
    S13 --> K6  
    S13 --> K7  
    S13 --> K8  
    S11 --> K9  
  
    K1 --> RG11  
    K2 --> RG11  
    K5 --> RG14  
    K6 --> RG14  
    K7 --> RG14  
    K8 --> FE4  
    K4 --> CT8  
    K3 --> CT8  
    K9 --> RG11  
  
    %% ---------------------------------------------------------  
    %% OBSERVABILITY + AUDIT STORY  
    %% ---------------------------------------------------------  
    subgraph AO[Observability and Audit Story]  
        A1[Stage entered]  
        A2[Runtime resolved]  
        A3[Tool invoked]  
        A4[Controller result returned]  
        A5[Review decision captured]  
        A6[Workflow state updated]  
        A7[Audit record persisted]  
        A8[Observability event persisted]  
        A9[Flow explorer updated]  
    end  
  
    A1 --> A2  
    A2 --> A3  
    A3 --> A4  
    A4 --> A5  
    A5 --> A6  
    A5 --> A7  
    A5 --> A8  
    A6 --> A9  
  
    CT8 --> A4  
    S15 --> A7  
    S14 --> A8  
    S13 --> A9  
  
    %% ---------------------------------------------------------  
    %% RESPONSE BACK TO FRONTEND  
    %% ---------------------------------------------------------  
    RC1 --> JB4  
    JB4 --> JB5  
    JB4 --> JB6  
    JB4 --> JB7  
    JB5 --> FE10  
    JB6 --> FE10  
    JB7 --> FE10  
    FE10 --> FE9  
    FE9 --> FE6  
    FE6 --> FE1  
    FE6 --> FE2  
    FE6 --> FE3  
    FE6 --> FE4  
    FE6 --> FE5  
  
    %% ---------------------------------------------------------  
    %% USER DECISION LOOP  
    %% ---------------------------------------------------------  
    FE2 --> U0  
    FE3 --> U0  
    U0 -->|Select / Comment / Preview / Approve / Reject / Escalate / Rerun| FE8  

# ECl model workflow  
  
flowchart TD  
    %% =========================================================  
    %% MASTER ECL AGENTIC AI DIAGRAM  
    %% CONTRACT + RESOLVER + ORCHESTRATION + WORKFLOW  
    %% IFRS 9 / ECL PROJECT  
    %% =========================================================  
  
    %% ---------------------------------------------------------  
    %% USER ENTRY  
    %% ---------------------------------------------------------  
    U0[User<br/>Developer / Validator / Finance / Business / Governance / Approver / Monitoring]  
    U0 --> U1[Open JupyterLab Governed Workspace]  
    U1 --> U2[Choose mode<br/>resume / new project / review / dashboard / flow explorer]  
    U2 --> U3[Frontend builds workspace request]  
  
    %% ---------------------------------------------------------  
    %% FRONTEND WORKSPACE LAYER  
    %% ---------------------------------------------------------  
    subgraph FE[Frontend Workspace Layer]  
        FE1[Workspace Shell<br/>Header + Main Area + 3 Panels + Optional Bottom]  
        FE2[Left Panel<br/>Navigation / Candidates / Sections / Filters / Flow Nodes]  
        FE3[Center Panel<br/>Proposal / Preview / Evidence / Diagnostics / Charts / Tables / Diff]  
        FE4[Right Panel<br/>Actions / Comments / Structured Edits / Rerun Params / Conditions]  
        FE5[Bottom Panel<br/>Trace / Audit / Raw Detail / Logs / Large Drilldown]  
        FE6[Chat Support Panel<br/>Advisory only]  
        FE7[Workspace Store]  
        FE8[Draft Store]  
        FE9[Renderer Registry<br/>Review / Dashboard / Flow / Wizard / Mixed]  
        FE10[Event Dispatcher]  
        FE11[Patch Merger]  
        FE12[Bridge Client]  
        FE13[Frontend Validation<br/>comment requirement / schema shape / candidate selection]  
        FE14[Loading + Error + Blocked + Refresh banners]  
    end  
  
    U3 --> FE1  
    FE1 --> FE2  
    FE1 --> FE3  
    FE1 --> FE4  
    FE1 --> FE5  
    FE1 --> FE6  
    FE1 --> FE7  
    FE1 --> FE8  
    FE2 --> FE10  
    FE3 --> FE10  
    FE4 --> FE10  
    FE5 --> FE10  
    FE6 --> FE10  
    FE10 --> FE13  
    FE13 --> FE12  
    FE12 --> FE11  
    FE11 --> FE7  
    FE9 --> FE3  
    FE9 --> FE4  
    FE14 --> FE1  
  
    %% ---------------------------------------------------------  
    %% FRONTEND EVENT / RESPONSE CONTRACT  
    %% ---------------------------------------------------------  
    subgraph FC[Frontend Contract Layer]  
        FC1[Widget Event Envelope<br/>event_id / event_type / workspace_id / panel_id / actor / payload / client_ts / client_meta]  
        FC2[Event Types<br/>LOAD_WORKSPACE / REFRESH_WORKSPACE / OPEN_REVIEW / SELECT_CANDIDATE / SELECT_NODE / PREVIEW_EDIT / SUBMIT_ACTION / REQUEST_ROUTE / OPEN_DETAIL]  
        FC3[Response Envelope<br/>status / message / workspace_id / server_ts / response_type / controller_result / workspace_patch / notifications / warnings / errors / refresh_required / new_refresh_token]  
        FC4[Workspace Patch Contract<br/>runtime_decision_patch / allowed_actions_patch / panel_patches / draft_state_patch / refresh_token]  
        FC5[UI Contracts<br/>ReviewShellContract / DashboardContract / FlowExplorerContract]  
    end  
  
    FE10 --> FC1  
    FC1 --> FC2  
    FE12 --> FC3  
    FC3 --> FC4  
    FC4 --> FE11  
    FC5 --> FE9  
  
    %% ---------------------------------------------------------  
    %% JUPYTER BRIDGE  
    %% ---------------------------------------------------------  
    subgraph JB[Jupyter Bridge Layer]  
        JB1[Jupyter Bridge]  
        JB2[Event Router]  
        JB3[Payload Mapper]  
        JB4[Review Payload Mapper]  
        JB5[Dashboard Payload Mapper]  
        JB6[Flow Payload Mapper]  
        JB7[Workspace Builder]  
        JB8[Workspace State Store]  
        JB9[Callback / Event Registry]  
    end  
  
    FE12 --> JB1  
    JB1 --> JB2  
    JB1 --> JB3  
    JB3 --> JB4  
    JB3 --> JB5  
    JB3 --> JB6  
    JB1 --> JB7  
    JB1 --> JB8  
    JB1 --> JB9  
  
    %% ---------------------------------------------------------  
    %% RUNTIME / RESOLUTION LAYER  
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
        RT12[Runtime Decision Output<br/>stage_name / actor_role / access_mode / preconditions_passed / missing_preconditions / allowed_tools / blocked_tools / review_required / approval_required / audit_required / auto_continue_allowed / recommended_ui_mode / recommended_interaction_mode / recommended_token_mode / recommended_next_routes / notes]  
    end  
  
    JB2 --> RT1  
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
    %% CONFIG / POLICY / ROUTING  
    %% ---------------------------------------------------------  
    subgraph CFG[Config and Policy Pack]  
        CFG1[Runtime Master]  
        CFG2[Stage Registry]  
        CFG3[Stage Tool Matrix]  
        CFG4[Stage Preconditions]  
        CFG5[Role Capabilities]  
        CFG6[Tool Groups / Virtual Groups]  
        CFG7[Governance Overlays]  
        CFG8[Retry Policies]  
        CFG9[Workflow Routes]  
        CFG10[Failure Routes]  
        CFG11[Domain Overlay<br/>ECL / PD / LGD / SICR / EAD / Stress]  
        CFG12[Role Overlay]  
        CFG13[Environment Overlay<br/>Dev / UAT / Prod]  
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
    %% CONTROLLER ORCHESTRATION  
    %% ---------------------------------------------------------  
    subgraph CT[Controller Orchestration Layer]  
        CT0[Base Controller<br/>resolve runtime / verify preconditions / verify tool allowance / normalize response / attach workflow patch / attach audit hint / attach observability hint]  
        CT1[Session Controller]  
        CT2[Workflow Controller]  
        CT3[Review Controller]  
        CT4[DataPrep Controller]  
        CT5[PD Controller]  
        CT6[FL PD Controller]  
        CT7[LGD Controller]  
        CT8[FL LGD Controller]  
        CT9[SICR Controller]  
        CT10[EAD Controller]  
        CT11[FL EAD Controller]  
        CT12[Impact Controller]  
        CT13[Sensitivity Controller]  
        CT14[Validation Controller]  
        CT15[Monitoring Controller]  
        CT16[Reporting Controller]  
        CT17[Controller Factory]  
    end  
  
    JB2 --> CT17  
    CT17 --> CT1  
    CT17 --> CT2  
    CT17 --> CT3  
    CT17 --> CT4  
    CT17 --> CT5  
    CT17 --> CT6  
    CT17 --> CT7  
    CT17 --> CT8  
    CT17 --> CT9  
    CT17 --> CT10  
    CT17 --> CT11  
    CT17 --> CT12  
    CT17 --> CT13  
    CT17 --> CT14  
    CT17 --> CT15  
    CT17 --> CT16  
  
    RT12 --> CT0  
    CT1 --> CT0  
    CT2 --> CT0  
    CT3 --> CT0  
    CT4 --> CT0  
    CT5 --> CT0  
    CT6 --> CT0  
    CT7 --> CT0  
    CT8 --> CT0  
    CT9 --> CT0  
    CT10 --> CT0  
    CT11 --> CT0  
    CT12 --> CT0  
    CT13 --> CT0  
    CT14 --> CT0  
    CT15 --> CT0  
    CT16 --> CT0  
  
    %% ---------------------------------------------------------  
    %% CONTROLLER RESPONSE CONTRACT  
    %% ---------------------------------------------------------  
    subgraph RC[Controller Response Contract]  
        RC1[Standard Result Envelope<br/>status / message / controller_name / action_name / data / warnings / errors / references / runtime_decision / workflow_patch / agent_hint / audit_hint / observability_hint]  
        RC2[Agent Hint<br/>reasoning_summary / recommended_next_action / requires_human_review / suggested_followup_functions / safe_to_continue]  
        RC3[Workflow Hint<br/>recommended_next_stage / state_patch / should_open_review / review_type]  
        RC4[Audit Hint<br/>should_write_audit / audit_type]  
        RC5[Observability Hint<br/>should_write_event / event_type]  
    end  
  
    CT0 --> RC1  
    RC1 --> RC2  
    RC1 --> RC3  
    RC1 --> RC4  
    RC1 --> RC5  
    RC1 --> JB3  
    JB3 --> FE12  
  
    %% ---------------------------------------------------------  
    %% SDK / SERVICE LAYER  
    %% ---------------------------------------------------------  
    subgraph SDK[SDK and Service Layer]  
        S1[Registry Service]  
        S2[Workflow Service]  
        S3[HITL Service]  
        S4[DataPrep Service]  
        S5[Spark DataPrep Service]  
        S6[Dataset Service]  
        S7[PD Service]  
        S8[FL PD Service]  
        S9[LGD Service]  
        S10[FL LGD Service]  
        S11[SICR Service]  
        S12[EAD Service]  
        S13[FL EAD Service]  
        S14[Impact Service]  
        S15[Sensitivity Service]  
        S16[Validation Service]  
        S17[Reporting Service]  
        S18[Monitoring Service]  
        S19[Knowledge Service]  
        S20[RAG / Retrieval Service]  
        S21[Flow Visualization Service]  
        S22[Observability Service]  
        S23[Audit Service]  
        S24[Policy Service]  
    end  
  
    CT1 --> S1  
    CT2 --> S2  
    CT2 --> S24  
    CT3 --> S3  
    CT4 --> S4  
    CT4 --> S5  
    CT4 --> S6  
    CT5 --> S7  
    CT6 --> S8  
    CT7 --> S9  
    CT8 --> S10  
    CT9 --> S11  
    CT10 --> S12  
    CT11 --> S13  
    CT12 --> S14  
    CT13 --> S15  
    CT14 --> S16  
    CT15 --> S18  
    CT16 --> S17  
    CT2 --> S19  
    CT2 --> S20  
    CT2 --> S21  
    CT0 --> S22  
    CT0 --> S23  
  
    %% ---------------------------------------------------------  
    %% REGISTRIES / STATE  
    %% ---------------------------------------------------------  
    subgraph RG[Registry and Persistent State]  
        R1[Project Registry]  
        R2[Run Registry]  
        R3[Workflow State Store]  
        R4[Review Registry]  
        R5[Dataset Registry]  
        R6[Dataset Snapshot Registry]  
        R7[Artifact Registry]  
        R8[PD Registry]  
        R9[FL PD Registry]  
        R10[LGD Registry]  
        R11[FL LGD Registry]  
        R12[SICR Registry]  
        R13[EAD Registry]  
        R14[FL EAD Registry]  
        R15[Impact Registry]  
        R16[Sensitivity Registry]  
        R17[Validation Registry]  
        R18[Monitoring Snapshot Registry]  
        R19[Knowledge Registry]  
        R20[Audit Store]  
        R21[Observability Event Store]  
        R22[Flow Graph / Timeline Store]  
    end  
  
    S1 --> R1  
    S1 --> R2  
    S2 --> R3  
    S3 --> R4  
    S6 --> R5  
    S6 --> R6  
    S17 --> R7  
    S7 --> R8  
    S8 --> R9  
    S9 --> R10  
    S10 --> R11  
    S11 --> R12  
    S12 --> R13  
    S13 --> R14  
    S14 --> R15  
    S15 --> R16  
    S16 --> R17  
    S18 --> R18  
    S19 --> R19  
    S23 --> R20  
    S22 --> R21  
    S21 --> R22  
  
    %% ---------------------------------------------------------  
    %% ECL DOMAIN WORKFLOW  
    %% ---------------------------------------------------------  
    subgraph WF[ECL Domain Workflow]  
        W1[Session Bootstrap]  
        W2[Workflow Bootstrap / Resume]  
        W3[Data Preparation Config]  
        W4[Data Preparation Execution]  
        W5[Data Readiness Check]  
        W6[Dataset Registration and Snapshot]  
        W7[PD Development]  
        W8[FL PD Development]  
        W9[LGD Development]  
        W10[FL LGD Development]  
        W11[SICR Development]  
        W12[EAD Development]  
        W13[FL EAD Development]  
        W14[Integrated ECL Engine Assembly]  
        W15[Impact Assessment]  
        W16[Sensitivity Analysis]  
        W17[Validation Scope Init]  
        W18[Validation Evidence Intake]  
        W19[Methodology Review]  
        W20[Data Validation Review]  
        W21[Assumption Review]  
        W22[Fitness Review]  
        W23[Validation Conclusion Review]  
        W24[Technical Reporting]  
        W25[Committee Pack]  
        W26[Approval / Signoff]  
        W27[Deployment Preparation]  
        W28[Monitoring Setup]  
        W29[Monitoring Snapshot Ingest]  
        W30[Monitoring KPI Refresh]  
        W31[Monitoring Breach Review]  
        W32[Annual Review Pack]  
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
    %% SERVICE MAPPING TO WORKFLOW  
    %% ---------------------------------------------------------  
    W3 --> S4  
    W4 --> S5  
    W5 --> S5  
    W6 --> S6  
    W7 --> S7  
    W8 --> S8  
    W9 --> S9  
    W10 --> S10  
    W11 --> S11  
    W12 --> S12  
    W13 --> S13  
    W14 --> S2  
    W15 --> S14  
    W16 --> S15  
    W17 --> S16  
    W18 --> S16  
    W19 --> S16  
    W20 --> S16  
    W21 --> S16  
    W22 --> S16  
    W23 --> S3  
    W23 --> S16  
    W24 --> S17  
    W25 --> S17  
    W26 --> S3  
    W27 --> S2  
    W28 --> S18  
    W29 --> S18  
    W30 --> S18  
    W31 --> S3  
    W31 --> S18  
    W32 --> S18  
    W32 --> S17  
  
    %% ---------------------------------------------------------  
    %% COMPONENT DETAIL SUBFLOW  
    %% ---------------------------------------------------------  
    subgraph CMP[Component Detail]  
        C1[PD<br/>default definition / sample / features / segmentation / baseline fit / discrimination / calibration / stability / benchmark]  
        C2[FL PD<br/>MEV sourcing / transformation / PCA or shortlist / scenario conditioning / path generation / reasonableness]  
        C3[LGD<br/>workout logic / recovery cashflow / discounting / segmentation / baseline fit / cyclicality]  
        C4[FL LGD<br/>macro linkage / ECM or scalar / recursive path / scenario conditioning / reasonableness]  
        C5[SICR<br/>relative PD / absolute PD / score deterioration / DPD backstop / threshold calibration / migration stability]  
        C6[EAD<br/>exposure path / utilization / CCF / segmentation / baseline fit]  
        C7[FL EAD<br/>macro linked utilization / scalar / scenario conditioned drawdown]  
        C8[Integrated Engine<br/>stage logic / scenario weights / horizon / discounting / aggregation / decomposition]  
        C9[Impact Assessment<br/>old vs new / portfolio / segment / stage migration / driver attribution / finance challenge]  
        C10[Sensitivity<br/>MEV / scenario weight / SICR threshold / parameter / segmentation / overlay]  
    end  
  
    W7 --> C1  
    W8 --> C2  
    W9 --> C3  
    W10 --> C4  
    W11 --> C5  
    W12 --> C6  
    W13 --> C7  
    W14 --> C8  
    W15 --> C9  
    W16 --> C10  
  
    %% ---------------------------------------------------------  
    %% HITL REVIEW LOOP  
    %% ---------------------------------------------------------  
    subgraph HITL[Governed HITL Loop]  
        H1[Agent / service produces proposal<br/>candidate / preview / diagnostics / conclusion option / breach view]  
        H2[Create review payload]  
        H3[Render governed workspace contract]  
        H4[Human selects candidate / section / node]  
        H5[Human previews edits]  
        H6[Human adds comments / conditions / challenge notes]  
        H7[Human approves / approves with conditions / rejects / escalates / reruns]  
        H8[Validate action against runtime decision]  
        H9[Capture decision]  
        H10[Patch workflow state]  
        H11[Write audit]  
        H12[Write observability event]  
        H13[Refresh workspace]  
    end  
  
    C1 --> H1  
    C2 --> H1  
    C3 --> H1  
    C4 --> H1  
    C5 --> H1  
    C6 --> H1  
    C7 --> H1  
    C8 --> H1  
    C9 --> H1  
    C10 --> H1  
    W23 --> H1  
    W31 --> H1  
  
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
  
    %% ---------------------------------------------------------  
    %% GOVERNANCE GATES  
    %% ---------------------------------------------------------  
    subgraph GV[Governance Gates]  
        G1{Preconditions satisfied?}  
        G2{Tool allowed?}  
        G3{Review required?}  
        G4{Approval required?}  
        G5{Audit required?}  
        G6{Missing active review / stale state / severe unresolved breach?}  
    end  
  
    RT12 --> G1  
    RT12 --> G2  
    RT12 --> G3  
    RT12 --> G4  
    RT12 --> G5  
    RT12 --> G6  
  
    G1 -->|No| FE14  
    G2 -->|No| FE14  
    G6 -->|Yes| FE14  
    G3 -->|Yes| H2  
    G4 -->|Yes| H7  
    G5 -->|Yes| H11  
  
    %% ---------------------------------------------------------  
    %% KNOWLEDGE / FLOW / OBSERVABILITY  
    %% ---------------------------------------------------------  
    subgraph KF[Knowledge, Flow, and Observability]  
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
  
    S19 --> K1  
    S19 --> K2  
    S19 --> K3  
    S20 --> K4  
    S21 --> K5  
    S21 --> K6  
    S21 --> K7  
    S21 --> K8  
    S19 --> K9  
  
    K1 --> R19  
    K2 --> R19  
    K5 --> R22  
    K6 --> R22  
    K7 --> R22  
    K8 --> FE5  
    K3 --> CT0  
    K4 --> CT0  
    K9 --> R19  
  
    %% ---------------------------------------------------------  
    %% FEEDBACK / REWORK LOOPS  
    %% ---------------------------------------------------------  
    DQ1{Data acceptable?}  
    PD1{PD acceptable?}  
    FPD1{FL PD acceptable?}  
    LGD1{LGD acceptable?}  
    FLGD1{FL LGD acceptable?}  
    SICR1{SICR acceptable?}  
    EAD1{EAD acceptable?}  
    FLEAD1{FL EAD acceptable?}  
    INT1{Integrated ECL acceptable?}  
    IMP1{Impact explainable?}  
    SEN1{Sensitivity acceptable?}  
    VAL1{Validation fit for use?}  
    APR1{Approved for deployment?}  
  
    W5 --> DQ1  
    DQ1 -->|No| W3  
    DQ1 -->|Yes| W6  
  
    W7 --> PD1  
    PD1 -->|No| W7  
    PD1 -->|Yes| W8  
  
    W8 --> FPD1  
    FPD1 -->|No| W8  
    FPD1 -->|Yes| W9  
  
    W9 --> LGD1  
    LGD1 -->|No| W9  
    LGD1 -->|Yes| W10  
  
    W10 --> FLGD1  
    FLGD1 -->|No| W10  
    FLGD1 -->|Yes| W11  
  
    W11 --> SICR1  
    SICR1 -->|No| W11  
    SICR1 -->|Yes| W12  
  
    W12 --> EAD1  
    EAD1 -->|No| W12  
    EAD1 -->|Yes| W13  
  
    W13 --> FLEAD1  
    FLEAD1 -->|No| W13  
    FLEAD1 -->|Yes| W14  
  
    W14 --> INT1  
    INT1 -->|No| W14  
    INT1 -->|Yes| W15  
  
    W15 --> IMP1  
    IMP1 -->|No| W14  
    IMP1 -->|Yes| W16  
  
    W16 --> SEN1  
    SEN1 -->|No| W14  
    SEN1 -->|Yes| W17  
  
    W23 --> VAL1  
    VAL1 -->|No| W7  
    VAL1 -->|No| W9  
    VAL1 -->|No| W11  
    VAL1 -->|No| W12  
    VAL1 -->|No| W14  
    VAL1 -->|Yes| W24  
  
    W26 --> APR1  
    APR1 -->|No| W17  
    APR1 -->|Yes| W27  

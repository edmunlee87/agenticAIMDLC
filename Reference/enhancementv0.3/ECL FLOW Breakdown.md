# ECL FLOW Breakdown  
  
## Below are 4 decomposed detailed Mermaid diagrams by section for the ECL project.  
##   
## They are split into:  
	1.	**Architecture + contract**  
	2.	**Runtime resolver + orchestration**  
	3.	**ECL model development workflow**  
	3.	**ECL model development workflow**  
	4.	**HITL + validation + approval + monitoring**  
  
⸻  
##   
**1) Architecture + contract**  
  
```
flowchart TD
    %% =========================================================
    %% SECTION 1
    %% ARCHITECTURE + CONTRACT
    %% =========================================================

    U0[User<br/>Developer / Validator / Finance / Business / Governance / Approver / Monitoring]
    U0 --> U1[Open JupyterLab Governed Workspace]
    U1 --> U2[Choose workspace mode<br
```
```
/>resume / new / review / dashboard / flow explorer]

```
```

    subgraph FE[Frontend Workspace Layer]
        FE1[Workspace Shell<br/>Header + Main Area + 3 Panels + Optional Bottom]
        FE2[Left Panel<br/>Navigation / Candidates / Sections / Filters / Flow Nodes]
        FE3[Center Panel<br
```
```
/>Proposal / Preview / Evidence / Diagnostics / Charts / Tables / Diff]

```
```
        FE4[Right Panel<br
```
```
/>Actions / Comments / Structured Edits / Rerun Params / Conditions]

```
```
        FE5[Bottom Panel<br
```
```
/>Trace / Raw Detail / Audit / Logs]

```
```
        FE6[Chat Support Panel<br/>Advisory only]
        FE7[Workspace Store]
        FE8[Draft Store]
        FE9[Renderer Registry<br/>Review / Dashboard / Flow / Wizard / Mixed]
        FE10[Event Dispatcher]
        FE11[Patch Merger]
        FE12[Bridge Client]
        FE13[Frontend Validation]
        FE14[Loading / Error / Blocked / Refresh banners]
    end

    U2 --> FE1
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

    subgraph FC[Frontend Event 
```
```
and Response Contract]

```
```
        FC1[Widget Event Envelope<br
```
```
/>event_id<br/>event_type<br/>workspace_id<br/>panel_id<br/>actor<br/>payload<br/>client_ts<br/>client_meta]

```
```
        FC2[Event Types<br/>LOAD_WORKSPACE<br/>REFRESH_WORKSPACE<br/>OPEN_REVIEW<br/>SELECT_CANDIDATE<br/>SELECT_NODE<br/>PREVIEW_EDIT<br/>SUBMIT_ACTION<br/>REQUEST_ROUTE<br/>OPEN_DETAIL]
        FC3[Response Envelope<br/>status<br/>message<br/>workspace_id<br/>server_ts<br/>response_type<br/>controller_result<br/>workspace_patch<br/>notifications<br/>warnings<br/>errors<br/>refresh_required<br/>new_refresh_token]
        FC4[Workspace Patch Contract<br/>runtime_decision_patch<br/>allowed_actions_patch<br/>panel_patches<br/>draft_state_patch<br/>refresh_token]
        FC5[UI Contracts<br/>ReviewShellContract<br/>DashboardContract<br/>FlowExplorerContract]
    end

    FE10 --> FC1
    FC1 --> FC2
    FE12 --> FC3
    FC3 --> FC4
    FC4 --> FE11
    FC5 --> FE9

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

    subgraph OUT[Backend Response Back 
```
```
to Frontend]

```
```
        O1[Full Workspace Response]
        O2[Workspace Patch Response]
        O3[Validation Result Response]
        O4[Notification Response]
    end

    JB3 --> O1
    JB3 --> O2
    JB3 --> O3
    JB3 --> O4

    O1 --> FE12
    O2 --> FE12
    O3 --> FE12
    O4 --> FE12

```
  
  
⸻  
##   
**2) Runtime resolver + orchestration**  
  
```
flowchart TD
    %% =========================================================
    %% SECTION 
```
```
2

```
```
    %% RUNTIME RESOLVER + ORCHESTRATION
    %% =========================================================

    A0[Incoming request from Jupyter Bridge] --> A1[Runtime Resolver]

    subgraph CFG[Config and Policy Pack]
        C1[Runtime Master]
        C2[Stage Registry]
        C3[Stage Tool Matrix]
        C4[Stage Preconditions]
        C5[Role Capabilities]
        C6[Tool Groups / Virtual Tool Groups]
        C7[Governance Overlays]
        C8[Retry Policies]
        C9[Workflow Routes]
        C10[Failure Routes]
        C11[Domain Overlay<br/>ECL / PD / LGD / SICR / EAD / Stress]
        C12[Role Overlay]
        C13[Environment Overlay<br/>Dev / UAT / Prod]
    
```
```
end

```
```

    subgraph RT[Runtime Resolution Layer]
        R1[Stage Config Resolver]
        R2[Role Config Resolver]
        R3[Tool Group Resolver]
        R4[Governance Rule Resolver]
        R5[Retry Policy Resolver]
        R6[Allowlist Resolver]
        R7[Precondition Checker]
        R8[UI Mode Resolver]
        R9[Interaction Mode Resolver]
        R10[Token Mode Resolver]
        R11[Runtime Decision Output]
    end

    A1 --> R1
    A1 --> R2
    A1 --> R3
    A1 --> R4
    A1 --> R5
    A1 --> R6
    A1 --> R7
    A1 --> R8
    A1 --> R9
    A1 --> R10

    C1 --> R1
    C2 --> R1
    C3 --> R6
    C4 --> R7
    C5 --> R2
    C6 --> R3
    C7 --> R4
    C8 --> R5
    C9 --> A1
    C10 --> A1
    C11 --> R1
    C11 --> R6
    C12 --> R2
    C12 --> R6
    C13 --> R4
    C13 --> R5

    R1 --> R11
    R2 --> R11
    R3 --> R11
    R4 --> R11
    R5 --> R11
    R6 --> R11
    R7 --> R11
    R8 --> R11
    R9 --> R11
    R10 --> R11

    subgraph GV[Governance Gates]
        G1{Preconditions satisfied?}
        G2{Tool allowed?}
        G3{Review required?}
        G4{Approval required?}
        G5{Audit required?}
        G6{Blocked by stale state / severe breach / missing active review?}
    end

    R11 --> G1
    R11 --> G2
    R11 --> G3
    R11 --> G4
    R11 --> G5
    R11 --> G6

    G1 -->
```
```
|No| B1[Return blocked / invalid response]

```
```
    G2 -->
```
```
|No| B1

```
```
    G6 -->
```
```
|Yes| B1

```
```

    G1 -->
```
```
|Yes| O0[Controller Factory]

```
```
    G2 -->|Yes| O0
    G6 -->
```
```
|No| O0

```
```

    subgraph CT[Controller Orchestration Layer]
        O0[Controller Factory]
        O1[Base Controller<br/>runtime checks + response envelope + workflow patch + audit + observability]
        O2[Session Controller]
        O3[Workflow Controller]
        O4[Review Controller]
        O5[DataPrep Controller]
        O6[PD Controller]
        O7[FL PD Controller]
        O8[LGD Controller]
        O9[FL LGD Controller]
        O10[SICR Controller]
        O11[EAD Controller]
        O12[FL EAD Controller]
        O13[Impact Controller]
        O14[Sensitivity Controller]
        O15[Validation Controller]
        O16[Monitoring Controller]
        O17[Reporting Controller]
    end

    O0 --> O2
    O0 --> O3
    O0 --> O4
    O0 --> O5
    O0 --> O6
    O0 --> O7
    O0 --> O8
    O0 --> O9
    O0 --> O10
    O0 --> O11
    O0 --> O12
    O0 --> O13
    O0 --> O14
    O0 --> O15
    O0 --> O16
    O0 --> O17

    O2 --> O1
    O3 --> O1
    O4 --> O1
    O5 --> O1
    O6 --> O1
    O7 --> O1
    O8 --> O1
    O9 --> O1
    O10 --> O1
    O11 --> O1
    O12 --> O1
    O13 --> O1
    O14 --> O1
    O15 --> O1
    O16 --> O1
    O17 --> O1

    subgraph SDK[SDK 
```
```
and Service Layer]

```
```
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
    
```
```
end

```
```

    O2 --> S1
    O3 --> S2
    O3 --> S24
    O4 --> S3
    O5 --> S4
    O5 --> S5
    O5 --> S6
    O6 --> S7
    O7 --> S8
    O8 --> S9
    O9 --> S10
    O10 --> S11
    O11 --> S12
    O12 --> S13
    O13 --> S14
    O14 --> S15
    O15 --> S16
    O16 --> S18
    O17 --> S17
    O3 --> S19
    O3 --> S20
    O3 --> S21
    O1 --> S22
    O1 --> S23

    subgraph RC[Controller Response Contract]
        RC1[Standard Result Envelope<br/>status / message / controller_name / action_name / data / warnings / errors / references / runtime_decision / workflow_patch / agent_hint / audit_hint / observability_hint]
        RC2[Agent Hint]
        RC3[Workflow Hint]
        RC4[Audit Hint]
        RC5[Observability Hint]
    
```
```
end

```
```

    O1 --> RC1
    RC1 --> RC2
    RC1 --> RC3
    RC1 --> RC4
    RC1 --> RC5

    RC1 --> Z0[Return result to Jupyter Bridge]
    B1 --> Z0

```
  
  
⸻  
##   
**3) ECL model development workflow**  
  
```
flowchart TD
    %% =========================================================
    %% SECTION 3
    %% ECL MODEL DEVELOPMENT WORKFLOW
    %% =========================================================

    A0[Start ECL Project 
```
```
Scope] --> A1[Define portfolios, components, horizons, staging logic]

```
```
    A1 --> A2[Build common data foundation]
    A2 --> A3[Data preparation config]
    A3 --> A4[Data preparation execution]
    A4 --> A5[Data readiness check]
    A5 --> A6{Data acceptable?}
    A6 -->|No| A3
    A6 -->|Yes| A7[Dataset registration and snapshot]

    %% PD
    subgraph PD[PD]
        P1[Define default definition]
        P2[Define observation unit and performance horizon]
        P3[Construct PD development sample]
        P4[Feature engineering and screening]
        P5[Segmentation strategy]
        P6[Baseline PD candidate models]
        P7[Discrimination tests]
        P8[Calibration tests]
        P9[Stability / OOT / benchmark]
        P10[PD final candidate]
    
```
```
end

```
```

    A7 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
    P5 --> P6
    P6 --> P7
    P7 --> P8
    P8 --> P9
    P9 --> P10

    P10 --> PG{PD acceptable?}
    PG -->|No| P3
    PG -->|Yes| FP1

    %% FL PD
    subgraph FLPD[Forward-Looking PD]
        FP1[Define FL PD architecture]
        FP2[Source macroeconomic variables]
        FP3[Transform MEVs<br/>lag / diff / yoy / qoq / standardization]
        FP4[Dimension reduction / shortlist]
        FP5[Construct FL PD dataset]
        FP6[Fit FL PD candidates]
        FP7[Scenario conditioning]
        FP8[Generate PD paths]
        FP9[Reasonableness / benchmark]
        FP10[FL PD final candidate]
    
```
```
end

```
```

    FP1 --> FP2
    FP2 --> FP3
    FP3 --> FP4
    FP4 --> FP5
    FP5 --> FP6
    FP6 --> FP7
    FP7 --> FP8
    FP8 --> FP9
    FP9 --> FP10

    FP10 --> FPG{FL PD acceptable?}
    FPG -->|No| FP2
    FPG -->|Yes| L1

    %% LGD
    subgraph LGD[LGD]
        L1[Define LGD target and workout logic]
        L2[Construct recovery cashflow dataset]
        L3[Collateral / guarantee / discounting treatment]
        L4[LGD segmentation]
        L5[Baseline LGD candidates]
        L6[Performance / stability / cyclicality review]
        L7[LGD final candidate]
    end

    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> L5
    L5 --> L6
    L6 --> L7

    L7 --> LG{LGD acceptable?}
    LG -->|No| L2
    LG -->|Yes| FLG1

    %% FL LGD
    subgraph FLLGD[Forward-Looking LGD]
        FLG1[Define FL LGD architecture]
        FLG2[Map MEVs to recovery / cure / severity]
        FLG3[Construct FL LGD dataset]
        FLG4[Fit FL LGD candidates]
        FLG5[Generate scenario-conditioned LGD paths]
        FLG6[Recursive path / mean reversion review]
        FLG7[Benchmark / reasonableness]
        FLG8[FL LGD final candidate]
    
```
```
end

```
```

    FLG1 --> FLG2
    FLG2 --> FLG3
    FLG3 --> FLG4
    FLG4 --> FLG5
    FLG5 --> FLG6
    FLG6 --> FLG7
    FLG7 --> FLG8

    FLG8 --> FLGG{FL LGD acceptable?}
    FLGG -->|No| FLG2
    FLGG -->|Yes| S1

    %% SICR
    subgraph SICR[SICR]
        S1[Define SICR framework]
        S2[Choose methodology<br/>relative PD / absolute PD / score / rating / hybrid]
        S3[
```
```
Include mandatory backstops]

```
```
        S4[Construct SICR sample]
        S5[Threshold calibration]
        S6[Stage migration stability review]
        S7[SICR final candidate]
    end

    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7

    S7 --> SG{SICR acceptable?}
    SG -->|No| S4
    SG -->|Yes| E1

    %% EAD
    subgraph EAD[EAD]
        E1[Define EAD scope and CCF logic]
        E2[Construct exposure and utilization dataset]
        E3[Segment by utilization behaviour]
        E4[Baseline EAD / CCF candidates]
        E5[Diagnostics / stability / benchmark]
        E6[EAD final candidate]
    end

    E1 --> E2
    E2 --> E3
    E3 --> E4
    E4 --> E5
    E5 --> E6

    E6 --> EG{EAD acceptable?}
    EG -->|No| E2
    EG -->|Yes| FE1

    %% FL EAD
    subgraph FLEAD[Forward-Looking EAD]
        FE1[Define FL EAD architecture]
        FE2[Map MEVs to drawdown / utilization / repayment]
        FE3[Construct FL EAD dataset]
        FE4[Fit FL EAD candidates]
        FE5[Scenario-conditioned EAD paths]
        FE6[Reasonableness / benchmark]
        FE7[FL EAD final candidate]
    
```
```
end

```
```

    FE1 --> FE2
    FE2 --> FE3
    FE3 --> FE4
    FE4 --> FE5
    FE5 --> FE6
    FE6 --> FE7

    FE7 --> FEG{FL EAD acceptable?}
    FEG -->|No| FE2
    FEG -->|Yes| X1

    %% INTEGRATION
    subgraph INT[Integrated ECL Engine]
        X1[Assemble stage logic]
        X2[Map PD / FL PD / LGD / FL LGD / SICR / EAD / FL EAD]
        X3[Define scenario weights]
        X4[Define discounting / horizon / maturity]
        X5[Run integrated ECL engine]
        X6[Generate outputs and decomposition]
        X7[Reconciliation and aggregation checks]
    
```
```
end

```
```

    X1 --> X2
    X2 --> X3
    X3 --> X4
    X4 --> X5
    X5 --> X6
    X6 --> X7

    X7 --> XG{Integrated ECL acceptable?}
    XG -->|No| X2
    XG -->|Yes| IA1

    %% IMPACT
    subgraph IMPACT[Impact Assessment]
        IA1[Old vs new comparison]
        IA2[Portfolio impact]
        IA3[Segment impact]
        IA4[Stage migration impact]
        IA5[PD / LGD / EAD attribution]
        IA6[MEV and scenario contribution]
        IA7[Top exposures review]
        IA8[Finance / business challenge]
    
```
```
end

```
```

    IA1 --> IA2
    IA2 --> IA3
    IA3 --> IA4
    IA4 --> IA5
    IA5 --> IA6
    IA6 --> IA7
    IA7 --> IA8

    IA8 --> IAG{Impact explainable?}
    IAG -->|No| X2
    IAG -->|Yes| SN1

    %% SENSITIVITY
    subgraph SENS[Sensitivity Analysis]
        SN1[Define sensitivity dimensions]
        SN2[MEV sensitivity]
        SN3[Scenario weight sensitivity]
        SN4[SICR threshold sensitivity]
        SN5[PD sensitivity]
        SN6[LGD sensitivity]
        SN7[EAD sensitivity]
        SN8[Overlay / segmentation sensitivity]
        SN9[Portfolio response analysis]
    end

    SN1 --> SN2
    SN2 --> SN3
    SN3 --> SN4
    SN4 --> SN5
    SN5 --> SN6
    SN6 --> SN7
    SN7 --> SN8
    SN8 --> SN9

    SN9 --> SNG{Sensitivity acceptable?}
    SNG -->|No| X2
    SNG -->|Yes| V1

    %% VALIDATION AND DEPLOYMENT
    subgraph VAL[Validation, Approval, Deployment]
        V1[Validation scope init]
        V2[Evidence intake]
        V3[Methodology review]
        V4[Data validation review]
        V5[Assumption review]
        V6[Fitness review]
        V7[Validation conclusion]
        V8[Technical report]
        V9[Committee pack]
        V10[Approval / signoff]
        V11[Deployment preparation]
        V12[Monitoring setup]
    
```
```
end

```
```

    V1 --> V2
    V2 --> V3
    V3 --> V4
    V4 --> V5
    V5 --> V6
    V6 --> V7
    V7 --> V8
    V8 --> V9
    V9 --> V10
    V10 --> V11
    V11 --> V12
```
```


```
  
  
⸻  
##   
**4) HITL + validation + approval + monitoring**  
  
```
flowchart TD
    %% =========================================================
    %% SECTION 4
    %% HITL + VALIDATION + APPROVAL + MONITORING
    %% =========================================================

    A0[Component or integrated proposal produced by agent / service] --> A1[Create review payload]
    A1 --> A2[Render governed review workspace]

    subgraph WS[Governed Workspace]
        W1[
```
```
Left Panel<br/>candidates / sections / node navigation]

```
```
        W2[Center Panel<br/>preview / evidence / diagnostics / benchmark / charts / tables]
        W3[
```
```
Right Panel<br/>approve / reject / escalate / rerun / comments / structured edits]

```
```
        W4[Bottom Panel<br/>trace / raw evidence / audit / logs]
    end

    A2 --> W1
    A2 --> W2
    A2 --> W3
    A2 --> W4

    W1 --> B1[Human selects candidate / section / node]
    B1 --> W2

    W3 --> B2{Human action}
    B2 -->|Preview edits| B3[Preview request]
    B3 --> B4[Backend recomputes preview]
    B4 --> B5[Patch center panel]
    B5 --> B2

    B2 -->|Approve| C1[Validate action]
    B2 -->|Approve with conditions| C1
    B2 -->|Reject| C1
    B2 -->|Escalate| C1
    B2 -->|Rerun with parameters| C1

    C1 --> C2{Valid and allowed?}
    C2 -->|No| C3[Return blocked / invalid response]
    C3 --> W3
    C2 -->|Yes| C4[Capture decision]

    C4 --> C5[Write audit record]
    C4 --> C6[Write observability event]
    C4 --> C7[Patch workflow state]
    C7 --> C8[Resolve next stage]
    C8 --> C9[Refresh workspace]

    %% VALIDATION
    subgraph VAL[Validation Flow]
        V1[Validation scope initialization]
        V2[Evidence intake and completeness review]
        V3[Methodology review]
        V4[Data validation review]
        V5[Assumption review]
        V6[Fitness-
```
```
for-use review]

```
```
        V7[Validation conclusion options]
        V8[Validation conclusion review]
        V9[Remediation action setup 
```
```
if required]

```
```
    
```
```
end

```
```

    C9 --> V1
    V1 --> V2
    V2 --> V3
    V3 --> V4
    V4 --> V5
    V5 --> V6
    V6 --> V7
    V7 --> V8
    V8 --> VG1{Fit for use?}
    VG1 -->|No| V9
    VG1 -->|Yes| P1[Proceed to committee and approval]
    V9 --> R1[Targeted redevelopment / rerun path]

    %% APPROVAL
    subgraph APP[Committee and Approval]
        P1[Technical report]
        P2[Executive summary and committee pack]
        P3[Formal approval / signoff]
    end

    P1 --> P2
    P2 --> P3
    P3 --> PG1{Approved?}
    PG1 -->|No| R1
    PG1 -->|Yes| M1[Deployment and monitoring setup]

    %% MONITORING
    subgraph MON[Monitoring and Closed Loop]
        M1[Monitoring framework configuration]
        M2[Periodic monitoring snapshot ingest]
        M3[KPI refresh<br/>calibration / stability / drift / stage migration / movement]
        M4[Threshold evaluation]
        M5{Breach detected?}
        M6[Monitoring breach review workspace]
        M7[Action note / remediation / escalation]
        M8[Annual review pack]
        M9[BAU continuous enhancement]
    
```
```
end

```
```

    M1 --> M2
    M2 --> M3
    M3 --> M4
    M4 --> M5
    M5 -->|No| M8
    M5 -->|Yes| M6
    M6 --> M7
    M7 --> M8
    M8 --> M9

    %% KNOWLEDGE / FLOW / AUDIT
    subgraph KF[Knowledge, Audit, Observability, Flow]
        K1[Capture knowledge from review event]
        K2[Capture knowledge from final decision]
        K3[Persist audit trail]
        K4[Persist observability event]
        K5[Build flow nodes / edges / timeline]
        K6[Flow explorer drilldown]
    
```
```
end

```
```

    C5 --> K3
    C6 --> K4
    C7 --> K5
    C4 --> K1
    V8 --> K2
    K5 --> K6

    %% REWORK LOOP
    R1 --> R2{Which area requires rework?}
    R2 -->|PD / FL PD| R3[Return to PD / FL PD development]
    R2 -->|LGD / FL LGD| R4[Return to LGD / FL LGD development]
    R2 -->|SICR| R5[Return to SICR development]
    R2 -->|EAD / FL EAD| R6[Return to EAD / FL EAD development]
    R2 -->|Integration / Impact / Sensitivity| R7[Return to integrated ECL and downstream analysis]
```
```


```
  
  
⸻  
##   
## If you want, I can next turn these 4 into:  
	•	a **clean executive version** for CRO / committee  
	•	or add **Mermaid class styling and color coding** so the diagrams look more professional.  
	•	or add **Mermaid class styling and color coding** so the diagrams look more professional.  

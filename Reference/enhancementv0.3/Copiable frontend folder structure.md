# Copiable frontend folder structure   
  
====================================================================  
COPIABLE FRONTEND FOLDER STRUCTURE + COMPONENT MAP  
JUPYTERLAB 3-PANEL HITL WORKSPACE  
AGENTIC AI MDLC FRAMEWORK  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This document provides a practical frontend folder structure and  
component map for implementing the JupyterLab governed workspace.  
  
It is designed to be:  
- modular  
- scalable  
- JupyterLab-friendly  
- React-friendly  
- contract-driven  
- easy to map to the backend bridge and controllers  
  
This should be used as the implementation starter layout for the  
frontend extension project.  
  
====================================================================  
1. RECOMMENDED PROJECT STRUCTURE  
====================================================================  
  
frontend/  
  package.json  
  tsconfig.json  
  webpack.config.js  
  style/  
    index.css  
    variables.css  
    layout.css  
    badges.css  
    panels.css  
    forms.css  
    tables.css  
    charts.css  
    banners.css  
  
  src/  
    index.ts  
    plugin.ts  
    tokens.ts  
    constants/  
      eventNames.ts  
      workspaceModes.ts  
      panelIds.ts  
      actionTypes.ts  
      statusTypes.ts  
      commandIds.ts  
  
    types/  
      common.ts  
      events.ts  
      contracts.ts  
      workspace.ts  
      runtime.ts  
      routing.ts  
      widgets.ts  
  
    services/  
      bridgeClient.ts  
      workspaceApi.ts  
      eventDispatcher.ts  
      patchMerger.ts  
      runtimeAdapter.ts  
      contractMapper.ts  
      layoutPersistence.ts  
      draftPersistence.ts  
      validationService.ts  
  
    store/  
      workspaceStore.ts  
      workspaceReducer.ts  
      workspaceSelectors.ts  
      draftStore.ts  
      uiStore.ts  
      notificationStore.ts  
  
    commands/  
      registerCommands.ts  
      workspaceCommands.ts  
      reviewCommands.ts  
      dashboardCommands.ts  
      flowCommands.ts  
  
    plugins/  
      mainWorkspacePlugin.ts  
      launcherPlugin.ts  
      statusBarPlugin.ts  
      commandPalettePlugin.ts  
      optionalSidebarPlugin.ts  
  
    shell/  
      WorkspaceShell.tsx  
      WorkspaceHeader.tsx  
      WorkspaceBody.tsx  
      PanelLayout.tsx  
      ResizeController.tsx  
  
    panels/  
      left/  
        LeftPanel.tsx  
        NavigationTree.tsx  
        CandidateList.tsx  
        CandidateCard.tsx  
        SectionTabs.tsx  
        FilterPanel.tsx  
        FlowNodeList.tsx  
  
      center/  
        CenterPanel.tsx  
        BlockRenderer.tsx  
        SummaryBlock.tsx  
        MetricGridBlock.tsx  
        ChartBlock.tsx  
        TableBlock.tsx  
        EvidenceBlock.tsx  
        DiffBlock.tsx  
        TrendBlock.tsx  
        NarrativeBlock.tsx  
        EmptyStateBlock.tsx  
        LoadingBlock.tsx  
  
      right/  
        RightPanel.tsx  
        ActionBar.tsx  
        ActionButton.tsx  
        CommentBox.tsx  
        StructuredEditForm.tsx  
        RerunParameterForm.tsx  
        ConditionsEditor.tsx  
        ApprovalSummary.tsx  
        ActionRequirements.tsx  
  
      bottom/  
        BottomPanel.tsx  
        DetailDrawer.tsx  
        RawDetailView.tsx  
        EvidenceTraceView.tsx  
        AuditTraceView.tsx  
        LogsView.tsx  
  
      chat/  
        ChatSupportPanel.tsx  
        ChatContextSummary.tsx  
        ChatSuggestionBox.tsx  
  
    workspaces/  
      review/  
        ReviewWorkspace.tsx  
        ReviewWorkspaceBuilder.ts  
        ReviewHeaderBadgeSet.tsx  
        ReviewWorkspaceMapper.ts  
  
      dashboard/  
        DashboardWorkspace.tsx  
        DashboardWorkspaceBuilder.ts  
        DashboardKpiGrid.tsx  
        DashboardTrendArea.tsx  
        DashboardFilterBar.tsx  
        DashboardNotesPanel.tsx  
  
      flow/  
        FlowWorkspace.tsx  
        FlowWorkspaceBuilder.ts  
        FlowGraphView.tsx  
        FlowTimelineView.tsx  
        FlowDetailPanel.tsx  
  
      wizard/  
        WizardWorkspace.tsx  
        WizardStepContainer.tsx  
        ResumeSelector.tsx  
        ProjectBootstrapCard.tsx  
  
      mixed/  
        MixedWorkspace.tsx  
        MixedWorkspaceBuilder.ts  
  
    renderers/  
      reviewShellRenderer.ts  
      dashboardRenderer.ts  
      flowRenderer.ts  
      widgetRendererRegistry.ts  
  
    hooks/  
      useWorkspaceState.ts  
      useRuntimeDecision.ts  
      useAllowedActions.ts  
      useEventDispatch.ts  
      useDraftState.ts  
      useRefreshToken.ts  
      usePanelLoading.ts  
      useOptimisticSelection.ts  
      useDebouncedComment.ts  
      useDebouncedFilters.ts  
  
    utils/  
      ids.ts  
      time.ts  
      guards.ts  
      deepMerge.ts  
      equality.ts  
      debounce.ts  
      throttle.ts  
      errorFormatter.ts  
      actionLabeling.ts  
      statusColoring.ts  
      workspaceModeHelpers.ts  
  
    test/  
      reducers/  
        workspaceReducer.test.ts  
        patchMerger.test.ts  
      services/  
        eventDispatcher.test.ts  
        bridgeClient.test.ts  
      components/  
        ActionBar.test.tsx  
        CommentBox.test.tsx  
        CandidateList.test.tsx  
      integration/  
        reviewFlow.test.tsx  
        dashboardFlow.test.tsx  
        flowExplorer.test.tsx  
  
====================================================================  
2. ENTRYPOINTS AND JUPYTERLAB PLUGINS  
====================================================================  
  
2.1 `src/index.ts`  
--------------------------------------------------------------------  
Purpose:  
- frontend package entrypoint  
- exports JupyterLab plugins  
  
Typical responsibility:  
- import all plugins  
- export plugin array  
  
2.2 `src/plugin.ts`  
--------------------------------------------------------------------  
Purpose:  
- central plugin registration hub  
- combine extension plugins in one place  
  
2.3 `src/plugins/mainWorkspacePlugin.ts`  
--------------------------------------------------------------------  
Purpose:  
- register main governed workspace widget in JupyterLab main area  
- main plugin for this project  
  
2.4 `src/plugins/launcherPlugin.ts`  
--------------------------------------------------------------------  
Purpose:  
- add launcher tile or menu action  
- let user open review/dashboard/flow workspace  
  
2.5 `src/plugins/statusBarPlugin.ts`  
--------------------------------------------------------------------  
Purpose:  
- status bar integration  
- show workspace status, sync state, draft indicator  
  
2.6 `src/plugins/commandPalettePlugin.ts`  
--------------------------------------------------------------------  
Purpose:  
- expose commands in command palette  
  
2.7 `src/plugins/optionalSidebarPlugin.ts`  
--------------------------------------------------------------------  
Purpose:  
- optional companion sidebar  
- keep it lightweight  
- do not make it core dependency  
  
====================================================================  
3. COMPONENT MAP BY AREA  
====================================================================  
  
--------------------------------------------------------------------  
3.1 MAIN AREA ROOT  
--------------------------------------------------------------------  
  
`WorkspaceShell.tsx`  
Purpose:  
- top-level shell in JupyterLab main area  
- receives workspace state  
- composes header, left, center, right, bottom panels  
  
Children:  
- WorkspaceHeader  
- WorkspaceBody  
- BottomPanel optional  
  
`WorkspaceHeader.tsx`  
Purpose:  
- render project/run/stage/role/status  
- show refresh button and quick commands  
  
`WorkspaceBody.tsx`  
Purpose:  
- render panel layout  
- manage split panes / resizing  
  
`PanelLayout.tsx`  
Purpose:  
- generic panel grid / layout logic  
- can support collapsed states  
  
`ResizeController.tsx`  
Purpose:  
- maintain left/right/bottom panel sizes  
- save layout preferences  
  
--------------------------------------------------------------------  
3.2 LEFT PANEL COMPONENTS  
--------------------------------------------------------------------  
  
`LeftPanel.tsx`  
Purpose:  
- wrapper for left panel content  
- decide whether to show navigation, candidates, filters, or nodes  
  
`NavigationTree.tsx`  
Purpose:  
- hierarchical nav tree  
- review sections, evidence sections, flow sections  
  
`CandidateList.tsx`  
Purpose:  
- render list of candidate cards  
  
`CandidateCard.tsx`  
Purpose:  
- render one candidate summary card  
- selected/unselected state  
- warning badges  
- compact metrics  
  
`SectionTabs.tsx`  
Purpose:  
- tab switcher for sections/categories  
  
`FilterPanel.tsx`  
Purpose:  
- dashboard / list filters  
  
`FlowNodeList.tsx`  
Purpose:  
- alternate left panel for flow explorer mode  
  
--------------------------------------------------------------------  
3.3 CENTER PANEL COMPONENTS  
--------------------------------------------------------------------  
  
`CenterPanel.tsx`  
Purpose:  
- wrapper for central content  
- hosts block renderer and workspace-specific views  
  
`BlockRenderer.tsx`  
Purpose:  
- schema-driven renderer for center blocks  
- dispatch block types to correct component  
  
`SummaryBlock.tsx`  
Purpose:  
- summary text / structured highlights  
  
`MetricGridBlock.tsx`  
Purpose:  
- KPI / metrics grid  
  
`ChartBlock.tsx`  
Purpose:  
- chart container wrapper  
- integrate chart lib later  
  
`TableBlock.tsx`  
Purpose:  
- render tables with paging or scroll  
  
`EvidenceBlock.tsx`  
Purpose:  
- evidence cards or evidence summaries  
  
`DiffBlock.tsx`  
Purpose:  
- compare previous/current  
- useful for preview changes  
  
`TrendBlock.tsx`  
Purpose:  
- dashboard time trends or monitoring trend visuals  
  
`NarrativeBlock.tsx`  
Purpose:  
- approved narrative text block display  
  
`EmptyStateBlock.tsx`  
Purpose:  
- no selection / no content state  
  
`LoadingBlock.tsx`  
Purpose:  
- skeletons / placeholders while loading  
  
--------------------------------------------------------------------  
3.4 RIGHT PANEL COMPONENTS  
--------------------------------------------------------------------  
  
`RightPanel.tsx`  
Purpose:  
- wrapper for decision and form controls  
  
`ActionBar.tsx`  
Purpose:  
- render allowed actions from backend  
- show action status, loading, disabled reasons  
  
`ActionButton.tsx`  
Purpose:  
- standardized action button  
- preview / approve / reject / escalate etc.  
  
`CommentBox.tsx`  
Purpose:  
- governed comment input  
- autosave draft support  
  
`StructuredEditForm.tsx`  
Purpose:  
- schema-driven structured edit rendering  
- core HITL editing component  
  
`RerunParameterForm.tsx`  
Purpose:  
- rerun / what-if input panel  
  
`ConditionsEditor.tsx`  
Purpose:  
- approve-with-conditions editor  
  
`ApprovalSummary.tsx`  
Purpose:  
- action impact / audit summary / approval state display  
  
`ActionRequirements.tsx`  
Purpose:  
- explains requirements:  
  - comment needed  
  - irreversible  
  - audit written  
  - approval required  
  
--------------------------------------------------------------------  
3.5 BOTTOM PANEL COMPONENTS  
--------------------------------------------------------------------  
  
`BottomPanel.tsx`  
Purpose:  
- collapsible bottom container  
  
`DetailDrawer.tsx`  
Purpose:  
- generic detail renderer  
  
`RawDetailView.tsx`  
Purpose:  
- raw metrics / raw payload / raw summaries  
  
`EvidenceTraceView.tsx`  
Purpose:  
- trace evidence links and lineage  
  
`AuditTraceView.tsx`  
Purpose:  
- audit detail viewer  
  
`LogsView.tsx`  
Purpose:  
- operational logs / event summaries  
  
--------------------------------------------------------------------  
3.6 CHAT PANEL COMPONENTS  
--------------------------------------------------------------------  
  
`ChatSupportPanel.tsx`  
Purpose:  
- optional assistant support panel inside workspace  
  
`ChatContextSummary.tsx`  
Purpose:  
- display current selected context for assistant  
  
`ChatSuggestionBox.tsx`  
Purpose:  
- suggested prompts or help actions  
  
====================================================================  
4. WORKSPACE MODE COMPONENT MAP  
====================================================================  
  
--------------------------------------------------------------------  
4.1 Review Mode  
--------------------------------------------------------------------  
  
Primary files:  
- `workspaces/review/ReviewWorkspace.tsx`  
- `workspaces/review/ReviewWorkspaceBuilder.ts`  
- `workspaces/review/ReviewWorkspaceMapper.ts`  
- `renderers/reviewShellRenderer.ts`  
  
Use:  
- governed HITL stages  
- model selection review  
- coarse classing review  
- validation conclusion review  
- monitoring breach review  
  
Panel mapping:  
- Left: NavigationTree + CandidateList  
- Center: BlockRenderer with review blocks  
- Right: ActionBar + CommentBox + StructuredEditForm  
  
--------------------------------------------------------------------  
4.2 Dashboard Mode  
--------------------------------------------------------------------  
  
Primary files:  
- `workspaces/dashboard/DashboardWorkspace.tsx`  
- `workspaces/dashboard/DashboardWorkspaceBuilder.ts`  
- `renderers/dashboardRenderer.ts`  
  
Use:  
- monitoring KPI dashboard  
- annual review dashboard  
- operational monitoring view  
  
Panel mapping:  
- Left: FilterPanel  
- Center: DashboardKpiGrid + DashboardTrendArea  
- Right: DashboardNotesPanel / actions  
  
--------------------------------------------------------------------  
4.3 Flow Explorer Mode  
--------------------------------------------------------------------  
  
Primary files:  
- `workspaces/flow/FlowWorkspace.tsx`  
- `workspaces/flow/FlowWorkspaceBuilder.ts`  
- `renderers/flowRenderer.ts`  
  
Use:  
- workflow visualization  
- audit flow  
- observability timeline  
  
Panel mapping:  
- Left: FlowNodeList  
- Center: FlowGraphView + FlowTimelineView  
- Right: FlowDetailPanel  
- Bottom: optional raw detail  
  
--------------------------------------------------------------------  
4.4 Wizard Mode  
--------------------------------------------------------------------  
  
Primary files:  
- `workspaces/wizard/WizardWorkspace.tsx`  
- `workspaces/wizard/ResumeSelector.tsx`  
- `workspaces/wizard/ProjectBootstrapCard.tsx`  
  
Use:  
- start new project  
- resume prior work  
- choose workspace route  
  
Panel mapping:  
- can simplify to center-focused layout  
- left/right optional/minimized  
  
--------------------------------------------------------------------  
4.5 Mixed Mode  
--------------------------------------------------------------------  
  
Primary files:  
- `workspaces/mixed/MixedWorkspace.tsx`  
- `workspaces/mixed/MixedWorkspaceBuilder.ts`  
  
Use:  
- technical build stages  
- non-governed but structured workspace  
  
====================================================================  
5. STORE MODULE MAP  
====================================================================  
  
`store/workspaceStore.ts`  
--------------------------------------------------------------------  
Purpose:  
- primary workspace state store  
- expose get/set/subscribe  
- likely one store per workspace_id  
  
`store/workspaceReducer.ts`  
--------------------------------------------------------------------  
Purpose:  
- reducer for all workspace actions  
- clean state transitions  
- patch merge logic  
  
`store/workspaceSelectors.ts`  
--------------------------------------------------------------------  
Purpose:  
- reusable selectors  
- avoid component-level state traversal  
  
`store/draftStore.ts`  
--------------------------------------------------------------------  
Purpose:  
- manage comment/edit/filter/rerun draft state  
- separate from authoritative state  
  
`store/uiStore.ts`  
--------------------------------------------------------------------  
Purpose:  
- layout preferences  
- panel collapse state  
- selected tabs  
- local-only UI toggles  
  
`store/notificationStore.ts`  
--------------------------------------------------------------------  
Purpose:  
- banners / toasts / alerts  
  
Recommended approach:  
- keep authoritative workspace state separate from local draft/UI state  
  
====================================================================  
6. SERVICE MODULE MAP  
====================================================================  
  
`services/bridgeClient.ts`  
--------------------------------------------------------------------  
Purpose:  
- low-level communication with backend Jupyter bridge  
  
Responsibilities:  
- send event envelope  
- receive response  
- normalize errors  
- include workspace_id and actor metadata  
  
`services/workspaceApi.ts`  
--------------------------------------------------------------------  
Purpose:  
- high-level API wrapper around bridgeClient  
- semantic methods like:  
  - loadWorkspace  
  - refreshWorkspace  
  - openReview  
  - submitAction  
  - previewEdit  
  - requestRoute  
  
`services/eventDispatcher.ts`  
--------------------------------------------------------------------  
Purpose:  
- main event dispatch service  
- receives UI intents  
- builds message envelopes  
- coordinates loading state and store updates  
  
`services/patchMerger.ts`  
--------------------------------------------------------------------  
Purpose:  
- central merge logic for workspace patches  
- apply backend patches safely  
- prevent stale overwrite  
  
`services/runtimeAdapter.ts`  
--------------------------------------------------------------------  
Purpose:  
- map backend runtime_decision to frontend-friendly helpers  
- e.g. allowed actions, badges, UI mode helpers  
  
`services/contractMapper.ts`  
--------------------------------------------------------------------  
Purpose:  
- normalize backend contracts to frontend render models  
  
`services/layoutPersistence.ts`  
--------------------------------------------------------------------  
Purpose:  
- save and restore panel sizes / collapsed states  
  
`services/draftPersistence.ts`  
--------------------------------------------------------------------  
Purpose:  
- save and restore safe local drafts  
  
`services/validationService.ts`  
--------------------------------------------------------------------  
Purpose:  
- lightweight frontend validation  
- comment required, required selection present, etc.  
  
====================================================================  
7. TYPE MODULE MAP  
====================================================================  
  
`types/common.ts`  
--------------------------------------------------------------------  
Shared common types:  
- ID aliases  
- generic patch types  
- notification types  
  
`types/events.ts`  
--------------------------------------------------------------------  
Protocol message types:  
- outbound envelopes  
- inbound response envelopes  
- event payload types  
  
`types/contracts.ts`  
--------------------------------------------------------------------  
UI contract types:  
- review shell  
- dashboard  
- flow explorer  
- block specs  
- action specs  
  
`types/workspace.ts`  
--------------------------------------------------------------------  
Workspace state types:  
- panel state  
- workspace state  
- draft state  
- ui state  
  
`types/runtime.ts`  
--------------------------------------------------------------------  
Runtime decision types:  
- allowed_tools  
- blocked_tools  
- review_required  
- approval_required  
- ui mode  
- interaction mode  
- token mode  
  
`types/routing.ts`  
--------------------------------------------------------------------  
Route transition and stage navigation types  
  
`types/widgets.ts`  
--------------------------------------------------------------------  
Widget-specific props and callback types  
  
====================================================================  
8. COMMAND MODULE MAP  
====================================================================  
  
`commands/registerCommands.ts`  
--------------------------------------------------------------------  
Purpose:  
- register all JupyterLab commands in one place  
  
`commands/workspaceCommands.ts`  
--------------------------------------------------------------------  
Commands:  
- open workspace  
- refresh workspace  
- close workspace  
- toggle bottom panel  
  
`commands/reviewCommands.ts`  
--------------------------------------------------------------------  
Commands:  
- open review  
- preview changes  
- submit primary action  
- clear draft  
  
`commands/dashboardCommands.ts`  
--------------------------------------------------------------------  
Commands:  
- open dashboard  
- refresh dashboard  
- save monitoring note  
  
`commands/flowCommands.ts`  
--------------------------------------------------------------------  
Commands:  
- open flow explorer  
- refresh flow  
- expand selected node detail  
  
====================================================================  
9. HOOK MODULE MAP  
====================================================================  
  
`hooks/useWorkspaceState.ts`  
--------------------------------------------------------------------  
Purpose:  
- subscribe to workspace store  
  
`hooks/useRuntimeDecision.ts`  
--------------------------------------------------------------------  
Purpose:  
- expose runtime decision helpers to components  
  
`hooks/useAllowedActions.ts`  
--------------------------------------------------------------------  
Purpose:  
- convenient action enablement logic  
  
`hooks/useEventDispatch.ts`  
--------------------------------------------------------------------  
Purpose:  
- wrap event dispatcher for React usage  
  
`hooks/useDraftState.ts`  
--------------------------------------------------------------------  
Purpose:  
- access/update draft state  
  
`hooks/useRefreshToken.ts`  
--------------------------------------------------------------------  
Purpose:  
- stale response protection  
  
`hooks/usePanelLoading.ts`  
--------------------------------------------------------------------  
Purpose:  
- panel loading indicators  
  
`hooks/useOptimisticSelection.ts`  
--------------------------------------------------------------------  
Purpose:  
- optimistic left-panel or flow-node selection  
  
`hooks/useDebouncedComment.ts`  
--------------------------------------------------------------------  
Purpose:  
- debounce comment draft syncing  
  
`hooks/useDebouncedFilters.ts`  
--------------------------------------------------------------------  
Purpose:  
- debounce dashboard filter changes  
  
====================================================================  
10. RENDERER MODULE MAP  
====================================================================  
  
`renderers/reviewShellRenderer.ts`  
--------------------------------------------------------------------  
Purpose:  
- map review contract to panel render model  
- build left/center/right view config  
  
`renderers/dashboardRenderer.ts`  
--------------------------------------------------------------------  
Purpose:  
- map dashboard contract to panel render model  
  
`renderers/flowRenderer.ts`  
--------------------------------------------------------------------  
Purpose:  
- map flow contract to panel render model  
  
`renderers/widgetRendererRegistry.ts`  
--------------------------------------------------------------------  
Purpose:  
- registry of block types to components  
- e.g. summary -> SummaryBlock, chart -> ChartBlock  
  
====================================================================  
11. WHAT EACH PANEL SHOULD RENDER  
====================================================================  
  
LEFT PANEL  
--------------------------------------------------------------------  
Primary components by mode:  
  
Review mode:  
- NavigationTree  
- CandidateList  
  
Dashboard mode:  
- FilterPanel  
- small summary groups  
  
Flow mode:  
- FlowNodeList  
- timeline quick nav  
  
CENTER PANEL  
--------------------------------------------------------------------  
Primary components by mode:  
  
Review mode:  
- BlockRenderer  
  
Dashboard mode:  
- DashboardKpiGrid  
- DashboardTrendArea  
  
Flow mode:  
- FlowGraphView  
- FlowTimelineView  
  
RIGHT PANEL  
--------------------------------------------------------------------  
Primary components by mode:  
  
Review mode:  
- ActionBar  
- CommentBox  
- StructuredEditForm  
- ConditionsEditor  
  
Dashboard mode:  
- DashboardNotesPanel  
- action shortcuts  
  
Flow mode:  
- FlowDetailPanel  
- maybe selected node metadata  
  
BOTTOM PANEL  
--------------------------------------------------------------------  
Used for:  
- raw details  
- trace views  
- logs  
- evidence drilldown  
- large tables  
  
====================================================================  
12. RECOMMENDED COMPONENT RESPONSIBILITY BOUNDARIES  
====================================================================  
  
Keep these components dumb/presentational:  
--------------------------------------------------------------------  
- CandidateCard  
- ActionButton  
- SummaryBlock  
- TrendBlock  
- NarrativeBlock  
- ApprovalSummary  
  
Keep these components state-aware/container-like:  
--------------------------------------------------------------------  
- WorkspaceShell  
- LeftPanel  
- CenterPanel  
- RightPanel  
- ReviewWorkspace  
- DashboardWorkspace  
- FlowWorkspace  
  
Keep logic centralized in services/store:  
--------------------------------------------------------------------  
- event dispatch  
- patch merge  
- runtime interpretation  
- draft persistence  
- validation  
- bridge communication  
  
This split will make the UI much easier to maintain.  
  
====================================================================  
13. SUGGESTED BACKEND-TO-FRONTEND MAPPING  
====================================================================  
  
Backend object -> Frontend module  
  
Review payload  
-> `ReviewWorkspaceMapper.ts`  
-> `reviewShellRenderer.ts`  
-> `ReviewWorkspace.tsx`  
  
Dashboard payload  
-> `dashboardRenderer.ts`  
-> `DashboardWorkspace.tsx`  
  
Flow payload  
-> `flowRenderer.ts`  
-> `FlowWorkspace.tsx`  
  
Runtime decision  
-> `runtimeAdapter.ts`  
-> `useRuntimeDecision.ts`  
-> `ActionBar.tsx`  
-> `WorkspaceHeader.tsx`  
  
Workspace patch  
-> `patchMerger.ts`  
-> `workspaceReducer.ts`  
  
====================================================================  
14. RECOMMENDED INITIAL IMPLEMENTATION ORDER  
====================================================================  
  
Phase 1 core files:  
--------------------------------------------------------------------  
1. `plugin.ts`  
2. `mainWorkspacePlugin.ts`  
3. `WorkspaceShell.tsx`  
4. `workspaceStore.ts`  
5. `workspaceReducer.ts`  
6. `bridgeClient.ts`  
7. `eventDispatcher.ts`  
8. `WorkspaceHeader.tsx`  
9. `LeftPanel.tsx`  
10. `CenterPanel.tsx`  
11. `RightPanel.tsx`  
12. `ReviewWorkspace.tsx`  
13. `ActionBar.tsx`  
14. `CommentBox.tsx`  
15. `StructuredEditForm.tsx`  
  
Phase 2:  
--------------------------------------------------------------------  
1. Dashboard workspace files  
2. Flow workspace files  
3. Bottom panel files  
4. patchMerger  
5. status bar plugin  
  
Phase 3:  
--------------------------------------------------------------------  
1. draft persistence  
2. layout persistence  
3. command palette plugin  
4. optional sidebar plugin  
5. richer block renderer  
  
====================================================================  
15. RECOMMENDED MINIMUM VIABLE FRONTEND  
====================================================================  
  
For MVP, build these only:  
  
Core:  
- `plugin.ts`  
- `mainWorkspacePlugin.ts`  
- `WorkspaceShell.tsx`  
- `WorkspaceHeader.tsx`  
- `PanelLayout.tsx`  
  
Store/services:  
- `workspaceStore.ts`  
- `workspaceReducer.ts`  
- `bridgeClient.ts`  
- `eventDispatcher.ts`  
- `patchMerger.ts`  
  
Panels:  
- `LeftPanel.tsx`  
- `CenterPanel.tsx`  
- `RightPanel.tsx`  
  
Review mode:  
- `ReviewWorkspace.tsx`  
- `NavigationTree.tsx`  
- `CandidateList.tsx`  
- `BlockRenderer.tsx`  
- `ActionBar.tsx`  
- `CommentBox.tsx`  
- `StructuredEditForm.tsx`  
  
Types:  
- `events.ts`  
- `contracts.ts`  
- `workspace.ts`  
- `runtime.ts`  
  
This is enough to get a governed review workspace running.  
  
====================================================================  
16. RECOMMENDED FUTURE FILES  
====================================================================  
  
Later enhancements can add:  
  
- `ComparisonWorkspace.tsx`  
- `ArtifactPreviewPanel.tsx`  
- `InlineDiffTable.tsx`  
- `NarrativeEditor.tsx`  
- `ApprovalHistoryPanel.tsx`  
- `SlaTimerBadge.tsx`  
- `EvidenceChecklist.tsx`  
- `FlowPlaybackController.tsx`  
  
====================================================================  
17. FINAL RECOMMENDATION  
====================================================================  
  
Best practical frontend architecture:  
--------------------------------------------------------------------  
- one main JupyterLab plugin for main-area workspace  
- React for panel internals  
- Lumino for shell/layout integration  
- centralized store + event dispatcher  
- contract-driven renderers  
- schema-driven right-panel forms  
- runtime-driven action enablement  
  
That gives the cleanest balance between:  
- JupyterLab compatibility  
- UX quality  
- governance safety  
- maintainability  
- scalability  
  
====================================================================  
18. NEXT BEST ARTIFACT  
====================================================================  
  
The most useful next artifact is a:  
  
COPIABLE TYPESCRIPT CODE SKELETON  
for:  
- `plugin.ts`  
- `WorkspaceShell.tsx`  
- `workspaceStore.ts`  
- `eventDispatcher.ts`  
- `bridgeClient.ts`  
- `ReviewWorkspace.tsx`  
- `ActionBar.tsx`  
  
That would be the best direct jump from design into implementation.  
====================================================================  
END OF FRONTEND FOLDER STRUCTURE + COMPONENT MAP  
====================================================================  

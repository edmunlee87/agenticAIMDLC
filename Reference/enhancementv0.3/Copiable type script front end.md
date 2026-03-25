# Copiable type script front end  
  
```
// ================================================================
// COPIABLE TYPESCRIPT CODE SKELETON
// JUPYTERLAB 3-PANEL HITL WORKSPACE
// AGENTIC AI MDLC FRAMEWORK
// ================================================================
//
// INCLUDED FILES
// ------------------------------------------------
// 1. src/plugin.ts
// 2. src/shell/WorkspaceShell.tsx
// 3. src/store/workspaceStore.ts
// 4. src/services/eventDispatcher.ts
// 5. src/services/bridgeClient.ts
// 6. src/workspaces/review/ReviewWorkspace.tsx
// 7. src/panels/right/ActionBar.tsx
//
// NOTES
// ------------------------------------------------
// - This is a starter skeleton, not a full production implementation.
// - It assumes React is used inside a JupyterLab extension.
// - It is written to be easy to expand into your real project.
// - You will still need to wire Lumino / ReactWidget integration,
//   backend endpoints, styling, and complete typing.
//
// ================================================================



// ================================================================
// FILE: src/types/runtime.ts
// ================================================================

export type WorkspaceMode =
  | 'review'
  | 'dashboard'
  | 'flow'
  | 'wizard'
  | 'mixed'
  | 'chat';

export type PanelId =
  | 'left_panel'
  | 'center_panel'
  | 'right_panel'
  | 'chat_panel'
  | 'bottom_panel';

export type RuntimeDecision = {
  stage_name: string;
  actor_role: string;
  access_mode?: string;
  preconditions_passed?: boolean;
  missing_preconditions?: string[];
  allowed_tools: string[];
  blocked_tools?: string[];
  review_required?: boolean;
  approval_required?: boolean;
  audit_required?: boolean;
  auto_continue_allowed?: boolean;
  recommended_ui_mode?: string;
  recommended_interaction_mode?: string;
  recommended_token_mode?: string;
  recommended_next_routes?: string[];
  notes?: string[];
};


// ================================================================
// FILE: src/types/events.ts
// ================================================================

export type WidgetEventType =
  | 'LOAD_WORKSPACE'
  | 'REFRESH_WORKSPACE'
  | 'OPEN_REVIEW'
  | 'SELECT_NODE'
  | 'SELECT_CANDIDATE'
  | 'TAB_CHANGED'
  | 'FILTER_CHANGED'
  | 'COMMENT_CHANGED'
  | 'PREVIEW_EDIT'
  | 'APPLY_EDIT'
  | 'SUBMIT_ACTION'
  | 'SAVE_DRAFT'
  | 'REQUEST_ROUTE'
  | 'OPEN_DETAIL'
  | 'HEARTBEAT';

export type ActorPayload = {
  actor_id: string;
  actor_role: string;
};

export type WidgetEventEnvelope = {
  event_id: string;
  event_type: WidgetEventType;
  workspace_id: string;
  panel_id: PanelId;
  actor: ActorPayload;
  payload: Record<string, unknown>;
  client_ts?: string;
  client_meta?: Record<string, unknown>;
};

export type BridgeResponse = {
  status:
    | 'success'
    | 'success_with_warning'
    | 'invalid_input'
    | 'blocked'
    | 'failed'
    | 'pending_human_review'
    | 'finalized'
    | 'preview_ready';
  message: string;
  workspace_id: string;
  server_ts?: string;
  response_type?: 'workspace_patch' | 'full_workspace' | 'notification' | 'validation_result';
  controller_result?: Record<string, unknown>;
  workspace_patch?: Record<string, unknown>;
  notifications?: Array<{ level: 'info' | 'warning' | 'error' | 'success'; message: string }>;
  warnings?: Array<Record<string, unknown>>;
  errors?: Array<Record<string, unknown>>;
  refresh_required?: boolean;
  new_refresh_token?: number;
};


// ================================================================
// FILE: src/types/contracts.ts
// ================================================================

export type ActionButtonSpec = {
  action_id: string;
  label: string;
  action_type: string;
  style_variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  requires_comment?: boolean;
  disabled?: boolean;
  tooltip?: string;
};

export type CandidateCardSpec = {
  candidate_id: string;
  title: string;
  subtitle?: string;
  metrics?: Array<Record<string, unknown>>;
  warnings?: string[];
  selected?: boolean;
};

export type DetailBlockSpec = {
  block_id: string;
  block_type: string;
  title: string;
  payload: Record<string, unknown>;
};

export type ReviewShellContract = {
  workspace_id: string;
  review_id: string;
  left_navigation_items: Array<Record<string, unknown>>;
  candidate_cards: CandidateCardSpec[];
  center_blocks: DetailBlockSpec[];
  action_buttons: ActionButtonSpec[];
  comment_box_enabled: boolean;
  structured_edit_schema: Record<string, unknown>;
  context_summary: Record<string, unknown>;
};


// ================================================================
// FILE: src/types/workspace.ts
// ================================================================

import type { RuntimeDecision, WorkspaceMode } from './runtime';
import type { ReviewShellContract } from './contracts';

export type PanelState = {
  visible: boolean;
  loading: boolean;
  title: string;
  selected_id?: string | null;
  error_message?: string | null;
  data: Record<string, unknown>;
};

export type DraftState = {
  comment: string;
  structured_edits: Record<string, unknown>;
  selected_candidate_id?: string | null;
  selected_node_id?: string | null;
  filters: Record<string, unknown>;
  rerun_parameters: Record<string, unknown>;
};

export type WorkspaceState = {
  workspace_id: string;
  mode: WorkspaceMode;
  project_id?: string;
  run_id?: string;
  review_id?: string;
  session_id?: string;
  runtime_context: Record<string, unknown>;
  runtime_decision: RuntimeDecision | null;
  allowed_actions: string[];
  left_panel: PanelState;
  center_panel: PanelState;
  right_panel: PanelState;
  chat_panel: PanelState;
  bottom_panel: PanelState;
  draft_state: DraftState;
  refresh_token: number;
  last_server_sync_ts?: string | null;
  review_contract?: ReviewShellContract | null;
};

export const createEmptyWorkspaceState = (
  workspaceId: string,
  mode: WorkspaceMode
): WorkspaceState => ({
  workspace_id: workspaceId,
  mode,
  runtime_context: {},
  runtime_decision: null,
  allowed_actions: [],
  left_panel: {
    visible: true,
    loading: false,
    title: 'Navigation',
    selected_id: null,
    error_message: null,
    data: {}
  },
  center_panel: {
    visible: true,
    loading: false,
    title: 'Main Content',
    selected_id: null,
    error_message: null,
    data: {}
  },
  right_panel: {
    visible: true,
    loading: false,
    title: 'Actions',
    selected_id: null,
    error_message: null,
    data: {}
  },
  chat_panel: {
    visible: true,
    loading: false,
    title: 'Assistant',
    selected_id: null,
    error_message: null,
    data: {}
  },
  bottom_panel: {
    visible: false,
    loading: false,
    title: 'Details',
    selected_id: null,
    error_message: null,
    data: {}
  },
  draft_state: {
    comment: '',
    structured_edits: {},
    selected_candidate_id: null,
    selected_node_id: null,
    filters: {},
    rerun_parameters: {}
  },
  refresh_token: 0,
  last_server_sync_ts: null,
  review_contract: null
});


// ================================================================
// FILE: src/utils/ids.ts
// ================================================================

export const createClientEventId = (): string =>
  `evt_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;

export const nowIso = (): string => new Date().toISOString();


// ================================================================
// FILE: src/services/bridgeClient.ts
// ================================================================

import type { BridgeResponse, WidgetEventEnvelope } from '../types/events';

export class BridgeClient {
  private readonly baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async sendEvent(event: WidgetEventEnvelope): Promise<BridgeResponse> {
    const response = await fetch(`${this.baseUrl}/jupyter-bridge/event`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(event)
    });

    if (!response.ok) {
      return {
        status: 'failed',
        message: `Bridge request failed with status ${response.status}`,
        workspace_id: event.workspace_id,
        response_type: 'notification',
        errors: [{ status: response.status }]
      };
    }

    return (await response.json()) as BridgeResponse;
  }

  async loadWorkspace(payload: {
    workspace_id: string;
    mode: string;
    runtime_context: Record<string, unknown>;
    seed_payload?: Record<string, unknown>;
  }): Promise<BridgeResponse> {
    const response = await fetch(`${this.baseUrl}/jupyter-bridge/workspace/load`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      return {
        status: 'failed',
        message: `Workspace load failed with status ${response.status}`,
        workspace_id: payload.workspace_id
      };
    }

    return (await response.json()) as BridgeResponse;
  }

  async refreshWorkspace(payload: {
    workspace_id: string;
    runtime_context: Record<string, unknown>;
    patch_payload?: Record<string, unknown>;
  }): Promise<BridgeResponse> {
    const response = await fetch(`${this.baseUrl}/jupyter-bridge/workspace/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      return {
        status: 'failed',
        message: `Workspace refresh failed with status ${response.status}`,
        workspace_id: payload.workspace_id
      };
    }

    return (await response.json()) as BridgeResponse;
  }
}


// ================================================================
// FILE: src/store/workspaceStore.ts
// ================================================================

import type { WorkspaceState } from '../types/workspace';

type WorkspaceListener = (state: WorkspaceState) => void;

export class WorkspaceStore {
  private state: WorkspaceState;
  private listeners: Set<WorkspaceListener>;

  constructor(initialState: WorkspaceState) {
    this.state = initialState;
    this.listeners = new Set();
  }

  getState(): WorkspaceState {
    return this.state;
  }

  setState(nextState: WorkspaceState): void {
    this.state = nextState;
    this.emit();
  }

  patchState(patch: Partial<WorkspaceState>): void {
    this.state = {
      ...this.state,
      ...patch
    };
    this.emit();
  }

  subscribe(listener: WorkspaceListener): () => void {
    this.listeners.add(listener);
    listener(this.state);

    return () => {
      this.listeners.delete(listener);
    };
  }

  private emit(): void {
    for (const listener of this.listeners) {
      listener(this.state);
    }
  }
}


// ================================================================
// FILE: src/services/eventDispatcher.ts
// ================================================================

import { createClientEventId, nowIso } from '../utils/ids';
import type { BridgeClient } from './bridgeClient';
import type { BridgeResponse, WidgetEventEnvelope, WidgetEventType } from '../types/events';
import type { PanelId } from '../types/runtime';
import type { WorkspaceStore } from '../store/workspaceStore';
import type { WorkspaceState } from '../types/workspace';

export class EventDispatcher {
  private readonly bridgeClient: BridgeClient;
  private readonly workspaceStore: WorkspaceStore;

  constructor(bridgeClient: BridgeClient, workspaceStore: WorkspaceStore) {
    this.bridgeClient = bridgeClient;
    this.workspaceStore = workspaceStore;
  }

  private buildEnvelope(
    eventType: WidgetEventType,
    panelId: PanelId,
    payload: Record<string, unknown>
  ): WidgetEventEnvelope {
    const state = this.workspaceStore.getState();
    const runtimeContext = state.runtime_context;

    return {
      event_id: createClientEventId(),
      event_type: eventType,
      workspace_id: state.workspace_id,
      panel_id: panelId,
      actor: {
        actor_id: String(runtimeContext['actor_id'] ?? 'unknown_actor'),
        actor_role: String(runtimeContext['active_role'] ?? 'unknown_role')
      },
      payload,
      client_ts: nowIso(),
      client_meta: {
        workspace_mode: state.mode,
        refresh_token: state.refresh_token
      }
    };
  }

  async dispatch(
    eventType: WidgetEventType,
    panelId: PanelId,
    payload: Record<string, unknown>
  ): Promise<BridgeResponse> {
    this.setPanelLoading(panelId, true);

    try {
      const envelope = this.buildEnvelope(eventType, panelId, payload);
      const response = await this.bridgeClient.sendEvent(envelope);
      this.applyResponse(response);
      return response;
    } finally {
      this.setPanelLoading(panelId, false);
    }
  }

  async loadWorkspace(input: {
    workspace_id: string;
    mode: WorkspaceState['mode'];
    runtime_context: Record<string, unknown>;
    seed_payload?: Record<string, unknown>;
  }): Promise<BridgeResponse> {
    const response = await this.bridgeClient.loadWorkspace(input);
    this.applyResponse(response);
    return response;
  }

  async refreshWorkspace(patchPayload?: Record<string, unknown>): Promise<BridgeResponse> {
    const state = this.workspaceStore.getState();
    const response = await this.bridgeClient.refreshWorkspace({
      workspace_id: state.workspace_id,
      runtime_context: state.runtime_context,
      patch_payload: patchPayload
    });
    this.applyResponse(response);
    return response;
  }

  private setPanelLoading(panelId: PanelId, loading: boolean): void {
    const state = this.workspaceStore.getState();
    const panelKey = panelId as keyof WorkspaceState;

    if (
      panelKey === 'left_panel' ||
      panelKey === 'center_panel' ||
      panelKey === 'right_panel' ||
      panelKey === 'chat_panel' ||
      panelKey === 'bottom_panel'
    ) {
      const panel = state[panelKey];
      this.workspaceStore.patchState({
        [panelKey]: {
          ...panel,
          loading
        }
      } as Partial<WorkspaceState>);
    }
  }

  private applyResponse(response: BridgeResponse): void {
    const current = this.workspaceStore.getState();

    if (
      typeof response.new_refresh_token === 'number' &&
      response.new_refresh_token < current.refresh_token
    ) {
      return;
    }

    if (response.response_type === 'full_workspace') {
      const workspaceState = response.workspace_patch?.['workspace_state'] as WorkspaceState | undefined;
      if (workspaceState) {
        this.workspaceStore.setState(workspaceState);
      }
      return;
    }

    if (response.response_type === 'workspace_patch') {
      const patch = response.workspace_patch ?? {};
      const nextState: WorkspaceState = {
        ...current,
        runtime_decision:
          (patch['runtime_decision_patch'] as WorkspaceState['runtime_decision']) ??
          current.runtime_decision,
        allowed_actions:
          (patch['allowed_actions_patch'] as string[]) ?? current.allowed_actions,
        draft_state: {
          ...current.draft_state,
          ...((patch['draft_state_patch'] as Record<string, unknown>) ?? {})
        },
        refresh_token: response.new_refresh_token ?? current.refresh_token,
        last_server_sync_ts: response.server_ts ?? current.last_server_sync_ts
      };

      const panelPatches = (patch['panel_patches'] as Record<string, any>) ?? {};

      if (panelPatches.left_panel) {
        nextState.left_panel = { ...current.left_panel, ...panelPatches.left_panel };
      }
      if (panelPatches.center_panel) {
        nextState.center_panel = { ...current.center_panel, ...panelPatches.center_panel };
      }
      if (panelPatches.right_panel) {
        nextState.right_panel = { ...current.right_panel, ...panelPatches.right_panel };
      }
      if (panelPatches.chat_panel) {
        nextState.chat_panel = { ...current.chat_panel, ...panelPatches.chat_panel };
      }
      if (panelPatches.bottom_panel) {
        nextState.bottom_panel = { ...current.bottom_panel, ...panelPatches.bottom_panel };
      }

      this.workspaceStore.setState(nextState);
      return;
    }

    if (response.refresh_required) {
      void this.refreshWorkspace();
    }
  }
}


// ================================================================
// FILE: src/panels/right/ActionBar.tsx
// ================================================================

import React from 'react';
import type { ActionButtonSpec } from '../../types/contracts';

export type ActionBarProps = {
  actions: ActionButtonSpec[];
  allowedTools: string[];
  isSubmitting?: boolean;
  onActionClick: (action: ActionButtonSpec) => void;
};

const normalizeToolName = (actionType: string): string => {
  switch (actionType) {
    case 'approve':
      return 'approve_review';
    case 'approve_with_conditions':
      return 'approve_review_with_conditions';
    case 'reject':
      return 'capture_review_decision';
    case 'escalate':
      return 'escalate_review';
    case 'accept_with_edits':
      return 'capture_review_decision';
    case 'rerun_with_parameters':
      return 'capture_review_decision';
    case 'finalize':
      return 'finalize_validation_conclusion';
    default:
      return actionType;
  }
};

export const ActionBar: React.FC<ActionBarProps> = ({
  actions,
  allowedTools,
  isSubmitting = false,
  onActionClick
}) => {
  return (
    <div className="mrk-ActionBar">
      {actions.map((action) => {
        const requiredTool = normalizeToolName(action.action_type);
        const allowed = allowedTools.includes(requiredTool);
        const disabled = Boolean(action.disabled || isSubmitting || !allowed);

        return (
          <button
            key={action.action_id}
            className={`mrk-ActionButton mrk-ActionButton--${action.style_variant ?? 'primary'}`}
            disabled={disabled}
            title={action.tooltip ?? (allowed ? '' : 'Action not allowed in current runtime state')}
            onClick={() => onActionClick(action)}
            type="button"
          >
            {isSubmitting ? 'Submitting...' : action.label}
          </button>
        );
      })}
    </div>
  );
};

export default ActionBar;


// ================================================================
// FILE: src/shell/WorkspaceShell.tsx
// ================================================================

import React, { useEffect, useMemo, useState } from 'react';
import type { WorkspaceStore } from '../store/workspaceStore';
import type { WorkspaceState } from '../types/workspace';
import { ReviewWorkspace } from '../workspaces/review/ReviewWorkspace';

export type WorkspaceShellProps = {
  workspaceStore: WorkspaceStore;
};

const WorkspaceHeader: React.FC<{ state: WorkspaceState }> = ({ state }) => {
  const runtime = state.runtime_decision;

  return (
    <div className="mrk-WorkspaceHeader">
      <div className="mrk-WorkspaceHeader__left">
        <strong>{state.project_id ?? 'No Project'}</strong>
        <span>{state.run_id ?? 'No Run'}</span>
        <span>{runtime?.stage_name ?? 'Unknown Stage'}</span>
        <span>{state.mode}</span>
      </div>

      <div className="mrk-WorkspaceHeader__right">
        <span>{runtime?.actor_role ?? 'Unknown Role'}</span>
        {runtime?.review_required ? <span>Review Required</span> : null}
        {runtime?.approval_required ? <span>Approval Required</span> : null}
      </div>
    </div>
  );
};

const LeftPanel: React.FC<{ state: WorkspaceState }> = ({ state }) => {
  const review = state.review_contract;

  return (
    <div className="mrk-Panel mrk-Panel--left">
      <h3>{state.left_panel.title}</h3>

      {review?.candidate_cards?.length ? (
        <ul>
          {review.candidate_cards.map((candidate) => (
            <li key={candidate.candidate_id}>
              <strong>{candidate.title}</strong>
              {candidate.subtitle ? <div>{candidate.subtitle}</div> : null}
            </li>
          ))}
        </ul>
      ) : (
        <div>No items.</div>
      )}
    </div>
  );
};

const CenterPanel: React.FC<{ state: WorkspaceState }> = ({ state }) => {
  const review = state.review_contract;

  return (
    <div className="mrk-Panel mrk-Panel--center">
      <h3>{state.center_panel.title}</h3>

      {review?.center_blocks?.length ? (
        review.center_blocks.map((block) => (
          <div key={block.block_id} className="mrk-Block">
            <h4>{block.title}</h4>
            <pre>{JSON.stringify(block.payload, null, 2)}</pre>
          </div>
        ))
      ) : (
        <div>No main content.</div>
      )}
    </div>
  );
};

const RightPanel: React.FC<{ children: React.ReactNode; state: WorkspaceState }> = ({
  children,
  state
}) => {
  return (
    <div className="mrk-Panel mrk-Panel--right">
      <h3>{state.right_panel.title}</h3>
      {children}
    </div>
  );
};

export const WorkspaceShell: React.FC<WorkspaceShellProps> = ({ workspaceStore }) => {
  const [state, setState] = useState<WorkspaceState>(workspaceStore.getState());

  useEffect(() => {
    return workspaceStore.subscribe(setState);
  }, [workspaceStore]);

  const content = useMemo(() => {
    switch (state.mode) {
      case 'review':
        return <ReviewWorkspace workspaceStore={workspaceStore} state={state} />;
      default:
        return (
          <div className="mrk-WorkspaceShell__fallback">
            Workspace mode not yet implemented: {state.mode}
          </div>
        );
    }
  }, [state, workspaceStore]);

  return (
    <div className="mrk-WorkspaceShell">
      <WorkspaceHeader state={state} />
      {content}
    </div>
  );
};

export default WorkspaceShell;


// ================================================================
// FILE: src/workspaces/review/ReviewWorkspace.tsx
// ================================================================

import React, { useMemo, useState } from 'react';
import type { WorkspaceStore } from '../../store/workspaceStore';
import type { WorkspaceState } from '../../types/workspace';
import type { ActionButtonSpec } from '../../types/contracts';
import { ActionBar } from '../../panels/right/ActionBar';
import { EventDispatcher } from '../../services/eventDispatcher';
import { BridgeClient } from '../../services/bridgeClient';

export type ReviewWorkspaceProps = {
  workspaceStore: WorkspaceStore;
  state: WorkspaceState;
};

const ReviewCommentBox: React.FC<{
  value: string;
  onChange: (value: string) => void;
}> = ({ value, onChange }) => {
  return (
    <div className="mrk-CommentBox">
      <label htmlFor="mrk-comment-box">Comment</label>
      <textarea
        id="mrk-comment-box"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={6}
      />
    </div>
  );
};

export const ReviewWorkspace: React.FC<ReviewWorkspaceProps> = ({
  workspaceStore,
  state
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const bridgeClient = useMemo(() => new BridgeClient('/api'), []);
  const eventDispatcher = useMemo(
    () => new EventDispatcher(bridgeClient, workspaceStore),
    [bridgeClient, workspaceStore]
  );

  const review = state.review_contract;

  const actions: ActionButtonSpec[] = review?.action_buttons ?? [];
  const comment = state.draft_state.comment ?? '';

  const onCommentChange = (nextValue: string): void => {
    workspaceStore.patchState({
      draft_state: {
        ...state.draft_state,
        comment: nextValue
      }
    });
  };

  const onActionClick = async (action: ActionButtonSpec): Promise<void> => {
    if (!state.review_id && !review?.review_id) {
      return;
    }

    setIsSubmitting(true);
    try {
      await eventDispatcher.dispatch('SUBMIT_ACTION', 'right_panel', {
        review_id: state.review_id ?? review?.review_id,
        action: action.action_type,
        comment,
        structured_edits: state.draft_state.structured_edits,
        selected_candidate_id: state.draft_state.selected_candidate_id
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="mrk-ReviewWorkspace">
      <div className="mrk-ReviewWorkspace__left">
        <h3>{state.left_panel.title}</h3>
        {review?.candidate_cards?.length ? (
          <ul className="mrk-CandidateList">
            {review.candidate_cards.map((candidate) => (
              <li
                key={candidate.candidate_id}
                className={
                  candidate.selected ? 'mrk-CandidateCard mrk-CandidateCard--selected' : 'mrk-CandidateCard'
                }
                onClick={() => {
                  workspaceStore.patchState({
                    draft_state: {
                      ...state.draft_state,
                      selected_candidate_id: candidate.candidate_id
                    }
                  });
                }}
              >
                <strong>{candidate.title}</strong>
                {candidate.subtitle ? <div>{candidate.subtitle}</div> : null}
              </li>
            ))}
          </ul>
        ) : (
          <div>No candidates available.</div>
        )}
      </div>

      <div className="mrk-ReviewWorkspace__center">
        <h3>{state.center_panel.title}</h3>
        {review?.center_blocks?.length ? (
          review.center_blocks.map((block) => (
            <div key={block.block_id} className="mrk-ContentBlock">
              <h4>{block.title}</h4>
              <pre>{JSON.stringify(block.payload, null, 2)}</pre>
            </div>
          ))
        ) : (
          <div>No review content available.</div>
        )}
      </div>

      <div className="mrk-ReviewWorkspace__right">
        <h3>{state.right_panel.title}</h3>

        <ActionBar
          actions={actions}
          allowedTools={state.allowed_actions}
          isSubmitting={isSubmitting}
          onActionClick={onActionClick}
        />

        <ReviewCommentBox value={comment} onChange={onCommentChange} />

        <div className="mrk-StructuredEditPlaceholder">
          <h4>Structured Edits</h4>
          <pre>{JSON.stringify(review?.structured_edit_schema ?? {}, null, 2)}</pre>
        </div>
      </div>
    </div>
  );
};

export default ReviewWorkspace;


// ================================================================
// FILE: src/plugin.ts
// ================================================================

import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ReactWidget } from '@jupyterlab/ui-components';
import React from 'react';

import { WorkspaceShell } from './shell/WorkspaceShell';
import { WorkspaceStore } from './store/workspaceStore';
import { createEmptyWorkspaceState } from './types/workspace';

class GovernedWorkspaceWidget extends ReactWidget {
  private readonly workspaceStore: WorkspaceStore;

  constructor() {
    super();

    const initialState = createEmptyWorkspaceState('ws_demo_001', 'review');
    initialState.project_id = 'demo_project';
    initialState.run_id = 'demo_run';
    initialState.session_id = 'demo_session';
    initialState.runtime_context = {
      actor_id: 'u001',
      active_role: 'governance',
      project_id: 'demo_project',
      run_id: 'demo_run',
      session_id: 'demo_session',
      stage_context: { active_stage: 'coarse_classing_review' }
    };
    initialState.runtime_decision = {
      stage_name: 'coarse_classing_review',
      actor_role: 'governance',
      allowed_tools: [
        'get_review',
        'build_review_payload',
        'validate_review_action',
        'approve_review',
        'approve_review_with_conditions',
        'escalate_review',
        'capture_review_decision'
      ],
      review_required: true,
      approval_required: true
    };
    initialState.allowed_actions = initialState.runtime_decision.allowed_tools;
    initialState.review_id = 'rev_demo_001';
    initialState.review_contract = {
      workspace_id: 'ws_demo_001',
      review_id: 'rev_demo_001',
      left_navigation_items: [],
      candidate_cards: [
        {
          candidate_id: 'cand_001',
          title: 'Candidate A',
          subtitle: 'Best tradeoff',
          selected: true,
          metrics: [{ metric_name: 'gini', metric_value: 0.42 }]
        },
        {
          candidate_id: 'cand_002',
          title: 'Candidate B',
          subtitle: 'More stable',
          selected: false,
          metrics: [{ metric_name: 'gini', metric_value: 0.40 }]
        }
      ],
      center_blocks: [
        {
          block_id: 'blk_001',
          block_type: 'summary',
          title: 'Review Summary',
          payload: {
            text: 'This is a demo review payload rendered in the center panel.'
          }
        }
      ],
      action_buttons: [
        {
          action_id: 'approve_btn',
          label: 'Approve',
          action_type: 'approve',
          style_variant: 'primary'
        },
        {
          action_id: 'approve_cond_btn',
          label: 'Approve with Conditions',
          action_type: 'approve_with_conditions',
          style_variant: 'secondary',
          requires_comment: true
        },
        {
          action_id: 'reject_btn',
          label: 'Reject',
          action_type: 'reject',
          style_variant: 'danger',
          requires_comment: true
        }
      ],
      comment_box_enabled: true,
      structured_edit_schema: {
        fields: [{ field_name: 'bin_group', field_type: 'list' }]
      },
      context_summary: {
        stage: 'coarse_classing_review',
        domain: 'scorecard'
      }
    };

    this.workspaceStore = new WorkspaceStore(initialState);
    this.addClass('mrk-GovernedWorkspaceWidget');
    this.title.label = 'Governed Workspace';
    this.title.closable = true;
  }

  render(): JSX.Element {
    return <WorkspaceShell workspaceStore={this.workspaceStore} />;
  }
}

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'modurisk-governed-workspace:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    const commandId = 'modurisk-governed-workspace:open';

    app.commands.addCommand(commandId, {
      label: 'Open Governed Workspace',
      execute: () => {
        const widget = new GovernedWorkspaceWidget();
        app.shell.add(widget, 'main');
        app.shell.activateById(widget.id);
      }
    });

    app.commands.execute(commandId).catch((err) => {
      console.error('Failed to open governed workspace:', err);
    });
  }
};


```

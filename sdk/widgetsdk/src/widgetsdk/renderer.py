"""widgetsdk.renderer -- renders ReviewWorkspace to terminal or Jupyter IPython HTML.

The renderer is environment-aware: in Jupyter it emits rich HTML; in terminal
it renders a compact ASCII layout.  Web mode emits a JSON structure for
consumption by a frontend component.
"""

from __future__ import annotations

import json
from typing import Any

from widgetsdk.models import ReviewWorkspace, WidgetMode


def render(workspace: ReviewWorkspace, force_mode: WidgetMode | None = None) -> str | Any:
    """Render the workspace to the appropriate output format.

    Args:
        workspace: :class:`ReviewWorkspace` to render.
        force_mode: Override :attr:`ReviewWorkspace.mode`.

    Returns:
        Rendered output (HTML string, terminal string, or JSON-serializable dict).
    """
    mode = force_mode or workspace.mode
    if mode == WidgetMode.JUPYTER:
        return _render_html(workspace)
    if mode == WidgetMode.WEB:
        return _render_json(workspace)
    return _render_terminal(workspace)


def _render_terminal(workspace: ReviewWorkspace) -> str:
    lines: list[str] = []
    sep = "=" * 70
    lines.append(sep)
    lines.append(f"  {workspace.title}")
    lines.append(sep)

    lines.append("\n[PANEL A — Proposal & Evidence]")
    for card in workspace.evidence_cards:
        lines.append(f"\n  {card.title}")
        if card.summary:
            lines.append(f"  {card.summary}")
        for k, v in card.metric_highlights.items():
            lines.append(f"    {k}: {v}")

    lines.append("\n[PANEL B — Review Form]")
    for field in workspace.form_fields:
        req = " *" if field.required else ""
        lines.append(f"  {field.label}{req}: [{field.field_type}]")

    lines.append("\n[PANEL C — Actions]")
    if workspace.governance_status:
        gs = workspace.governance_status
        lines.append(f"  Policy: {gs.policy_status.upper()}")
        for reason in gs.blocking_reasons:
            lines.append(f"  !! {reason}")
    for btn in workspace.action_buttons:
        primary = " [PRIMARY]" if btn.is_primary else ""
        disabled = " [DISABLED]" if btn.disabled else ""
        lines.append(f"  [{btn.action_id}] {btn.label}{primary}{disabled}")

    lines.append(sep)
    return "\n".join(lines)


def _render_json(workspace: ReviewWorkspace) -> dict[str, Any]:
    return json.loads(workspace.model_dump_json())


def _render_html(workspace: ReviewWorkspace) -> Any:
    """Render as IPython HTML object for Jupyter display."""
    cards_html = ""
    for card in workspace.evidence_cards:
        highlights = "".join(
            f"<tr><td><b>{k}</b></td><td>{v}</td></tr>"
            for k, v in card.metric_highlights.items()
        )
        if highlights:
            highlights = f"<table style='font-size:12px;margin:4px 0;border-collapse:collapse'>{highlights}</table>"
        cards_html += (
            f"<div style='border:1px solid #ccc;border-radius:4px;padding:8px;margin:4px 0;background:#fafafa'>"
            f"<b>{card.title}</b><br><small>{card.summary}</small>{highlights}</div>"
        )

    fields_html = ""
    for field in workspace.form_fields:
        req = " <span style='color:red'>*</span>" if field.required else ""
        if field.field_type == "textarea":
            fields_html += (
                f"<div style='margin:6px 0'><label>{field.label}{req}</label>"
                f"<textarea style='width:100%;height:60px;margin-top:2px;padding:4px;"
                f"border:1px solid #ccc;border-radius:3px'>{field.value or ''}</textarea>"
                f"<small style='color:#888'>{field.help_text}</small></div>"
            )
        elif field.field_type == "checkbox":
            checked = "checked" if field.value else ""
            fields_html += (
                f"<div style='margin:6px 0'><input type='checkbox' {checked}>"
                f" <label>{field.label}{req}</label></div>"
            )

    gov_html = ""
    if workspace.governance_status:
        gs = workspace.governance_status
        color = {"ok": "#5cb85c", "warning": "#f0ad4e", "blocking": "#d9534f"}.get(gs.policy_status, "#aaa")
        reasons_html = "".join(f"<li>{r}</li>" for r in gs.blocking_reasons)
        gov_html = (
            f"<div style='background:{color};color:white;padding:4px 8px;border-radius:3px;font-size:12px'>"
            f"<b>Policy: {gs.policy_status.upper()}</b>"
            f"{'<ul style=margin:2px>' + reasons_html + '</ul>' if reasons_html else ''}</div>"
        )

    btns_html = ""
    for btn in workspace.action_buttons:
        bg = "#337ab7" if btn.is_primary else "#d9534f" if btn.is_destructive else "#5cb85c"
        if btn.disabled:
            bg = "#aaa"
        btns_html += (
            f"<button style='background:{bg};color:white;border:none;padding:6px 14px;"
            f"border-radius:3px;margin:3px;cursor:pointer' title='{btn.tooltip}'>"
            f"{btn.label}</button>"
        )

    html = f"""
<div style='font-family:monospace;border:2px solid #333;border-radius:6px;padding:0;overflow:hidden'>
  <div style='background:#333;color:white;padding:8px 12px;font-weight:bold'>{workspace.title}</div>
  <div style='display:flex;gap:0;min-height:300px'>
    <div style='flex:1;padding:12px;border-right:1px solid #ddd;background:#f9f9f9'>
      <b>{workspace.panel_a_title}</b><br>{cards_html}
    </div>
    <div style='flex:1;padding:12px;border-right:1px solid #ddd'>
      <b>Review Form</b><br>{fields_html}
    </div>
    <div style='flex:0 0 220px;padding:12px;background:#f0f0f0'>
      <b>Actions</b><br>{gov_html}<br>{btns_html}
    </div>
  </div>
</div>"""

    try:
        from IPython.display import HTML
        return HTML(html)
    except ImportError:
        return html

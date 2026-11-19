# -*- coding: utf-8 -*-
"""
DOM & Accessibility Tree Parser for NanoPro Operator.
Extracts interactive element semantics, roles, coordinates, and hierarchy
for consumption by Vision-Language Models.
"""

from typing import List, Dict, Any, Optional

EXTRACT_DOM_JS = r"""
() => {
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) return false;
    if (r.bottom < -50 || r.top > window.innerHeight * 1.5) return false;
    const style = window.getComputedStyle(el);
    return style.visibility !== 'hidden' && style.display !== 'none' && style.opacity !== '0';
  };

  const selector = [
    'a[href]', 'button', 'input', 'textarea', 'select', 'summary',
    '[role="button"]', '[role="link"]', '[role="tab"]', '[role="menuitem"]',
    '[role="checkbox"]', '[role="radio"]', '[contenteditable="true"]',
    '[onclick]', '[tabindex]:not([tabindex="-1"])'
  ].join(',');

  const nodes = Array.from(document.querySelectorAll(selector));
  const elements = [];

  for (const el of nodes) {
    if (!isVisible(el)) continue;

    const tag = el.tagName.toLowerCase();
    const type = (el.getAttribute('type') || '').toLowerCase();
    const role = el.getAttribute('role') || tag;
    const r = el.getBoundingClientRect();

    let label = el.innerText || '';
    if (!label.trim()) {
      if (el.id) {
        const lbl = document.querySelector(`label[for="${CSS.escape(el.id)}"]`);
        if (lbl) label = lbl.innerText || '';
      }
      if (!label.trim()) {
        const parentLabel = el.closest('label');
        if (parentLabel) label = parentLabel.innerText || '';
      }
    }

    if (!label.trim()) {
      label = el.getAttribute('aria-label') ||
              el.getAttribute('placeholder') ||
              el.getAttribute('title') ||
              el.getAttribute('name') ||
              el.getAttribute('alt') ||
              el.getAttribute('value') || '';
    }

    label = String(label).replace(/\s+/g, ' ').trim().slice(0, 100);

    // Value masking for safety (never expose passwords)
    let val = '';
    if (tag === 'input' || tag === 'textarea' || tag === 'select') {
      if (type === 'password') {
        val = '********';
      } else {
        val = String(el.value || '').slice(0, 50);
      }
    }

    elements.push({
      i: elements.length,
      tag: tag,
      role: role,
      type: type,
      label: label,
      value: val,
      disabled: el.disabled || el.getAttribute('aria-disabled') === 'true',
      checked: el.checked || el.getAttribute('aria-checked') === 'true',
      box: {
        x: Math.round(r.left),
        y: Math.round(r.top),
        w: Math.round(r.width),
        h: Math.round(r.height),
        cx: Math.round(r.left + r.width / 2),
        cy: Math.round(r.top + r.height / 2)
      }
    });

    if (elements.length >= 160) break;
  }

  return {
    title: document.title || '',
    url: window.location.href,
    elements: elements,
    innerTextSummary: (document.body ? document.body.innerText : '').slice(0, 4000)
  };
}
"""


class DOMTreeParser:
    """
    Parses and formats DOM & Accessibility trees for VLM reasoning.
    """

    @staticmethod
    def format_elements_for_llm(elements: List[Dict[str, Any]]) -> str:
        """
        Formats elements as a concise markdown list:
        [id] <tag/role> "label" (type=..., value=...) at (x, y, w, h)
        """
        lines = []
        for el in elements:
            idx = el.get("i", 0)
            tag = el.get("tag", "div")
            role = el.get("role", tag)
            lbl = el.get("label", "")
            val = el.get("value", "")
            box = el.get("box", {})
            cx = box.get("cx", 0)
            cy = box.get("cy", 0)

            attrs = []
            if el.get("type"):
                attrs.append(f"type={el['type']}")
            if val:
                attrs.append(f"value=\"{val}\"")
            if el.get("disabled"):
                attrs.append("DISABLED")
            if el.get("checked"):
                attrs.append("CHECKED")

            attr_str = f" ({', '.join(attrs)})" if attrs else ""
            label_str = f" \"{lbl}\"" if lbl else ""
            lines.append(f"[{idx}] <{role}>{label_str}{attr_str} -> Center: ({cx}, {cy})")

        return "\n".join(lines) if lines else "(No interactive elements found)"


dom_parser = DOMTreeParser()

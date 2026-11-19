# -*- coding: utf-8 -*-
"""
Set-of-Marks (SoM) Visual Marker module.
Renders high-visibility numbered bounding boxes and tags on browser/desktop screenshots.
This provides the Vision LLM with deterministic interactive targets, eliminating pixel coordinate drift.
"""

import io
from typing import List, Dict, Any, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont


class SetOfMarksAnnotator:
    """
    Overlays numbered pill markers and bounding rectangles onto screenshots
    for high-precision Vision-Language Model grounding.
    """

    COLOR_PALETTE = [
        ("#10B981", "#052e16"),  # Emerald Green
        ("#38BDF8", "#082f49"),  # Sky Blue
        ("#F59E0B", "#451a03"),  # Amber
        ("#EC4899", "#500724"),  # Pink
        ("#8B5CF6", "#2e1065"),  # Purple
        ("#14B8A6", "#042f2e"),  # Teal
    ]

    def __init__(self, font_size: int = 12):
        self.font_size = font_size
        try:
            # Try to load Windows standard font
            self.font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            self.font = ImageFont.load_default()

    def annotate(
        self,
        image_bytes: bytes,
        elements: List[Dict[str, Any]],
        draw_laser_cursor: Optional[Tuple[int, int]] = None
    ) -> Tuple[bytes, Image.Image]:
        """
        Draws numbered badges onto image copy and returns JPEG bytes and PIL Image.
        Each element in `elements` must contain:
            - 'i': integer index
            - 'box': {'x': float, 'y': float, 'w': float, 'h': float}
            - 'tag': optional tag name (e.g. 'button', 'input')
            - 'label': optional text label
        """
        base_img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
        overlay = Image.new("RGBA", base_img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        for el in elements:
            idx = el.get("i", 0)
            box = el.get("box", {})
            x = int(box.get("x", 0))
            y = int(box.get("y", 0))
            w = int(box.get("w", 0))
            h = int(box.get("h", 0))

            if w <= 0 or h <= 0:
                continue

            # Pick color variant deterministically based on index
            border_color, text_color = self.COLOR_PALETTE[idx % len(self.COLOR_PALETTE)]

            # 1. Draw subtle bounding box with rounded corners or dashed stroke
            draw.rectangle(
                [x, y, x + w, y + h],
                outline=border_color,
                width=2
            )

            # 2. Draw high-visibility numbered pill badge
            label_text = f"[{idx}]"
            bbox = self.font.getbbox(label_text)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            badge_padding_x = 4
            badge_padding_y = 2
            badge_w = text_w + (badge_padding_x * 2)
            badge_h = text_h + (badge_padding_y * 2)

            badge_x = max(0, x - 2)
            badge_y = max(0, y - badge_h - 2)

            # Draw badge background
            draw.rounded_rectangle(
                [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
                radius=3,
                fill=border_color
            )

            # Draw text number
            draw.text(
                (badge_x + badge_padding_x, badge_y + badge_padding_y - 1),
                label_text,
                font=self.font,
                fill=text_color
            )

        # 3. If laser cursor coordinates supplied, draw pulsating laser mouse cursor
        if draw_laser_cursor:
            cx, cy = draw_laser_cursor
            # Outer ripple halo
            draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], outline="#EF4444", width=2)
            draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill="#EF4444")
            draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill="#FFFFFF")

        # Composite overlay
        annotated = Image.alpha_composite(base_img, overlay).convert("RGB")

        buf = io.BytesIO()
        annotated.save(buf, format="JPEG", quality=85)
        return buf.getvalue(), annotated


som_marker = SetOfMarksAnnotator()

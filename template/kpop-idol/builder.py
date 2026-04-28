#!/usr/bin/env python3
#!/usr/bin/env python3
from __future__ import annotations
import re


def replace_placeholders(text, variables):
    if not isinstance(text, str):
        return text
    for key, value in variables.items():
        text = text.replace(f"[{key}]", value)
    return text


def default_template_to_prompt(template, variables, endpoint_provider=None):
    variables = variables or {}
    parts = []

    def process_dict_fields(d, prefix="", skip_defaults=True):
        for key, value in d.items():
            if skip_defaults and key == "defaults":
                continue
            if isinstance(value, str):
                value = replace_placeholders(value, variables)
                if value:
                    parts.append(f"{prefix}{key}: {value}".strip())
            elif isinstance(value, list):
                str_items = [replace_placeholders(v, variables) if isinstance(v, str) else str(v) if isinstance(v, (int, float)) else '' for v in value]
                str_items = [s for s in str_items if s]
                if str_items:
                    parts.append(f"{prefix}{key}: {', '.join(str_items)}".strip())
            elif isinstance(value, dict):
                process_dict_fields(value, f"{prefix}{key} - ", skip_defaults=False)

    for key, value in template.items():
        if key in ["defaults", "quality", "aspect_ratio", "longest side", "negative", "typography", "subject"]:
            continue
        if isinstance(value, dict):
            process_dict_fields(value)
        elif isinstance(value, str):
            value = replace_placeholders(value, variables)
            if value:
                parts.append(value)

    if "subject" in template:
        subj = template["subject"]
        if isinstance(subj, dict):
            desc = replace_placeholders(subj.get("描述", ""), variables)
            if desc:
                parts.append(f"Subject: {desc}")

    if "typography" in template:
        logic = replace_placeholders(template["typography"].get("排版逻辑", ""), variables)
        if logic:
            parts.append(f"Typography: {logic}")

    if "negative" in template:
        avoids = template["negative"].get("避免", [])
        if avoids:
            parts.append(f"Avoid: {', '.join(avoids)}")

    parts.append("masterpiece, best quality")
    prompt = ". ".join(parts)
    leftovers = re.findall(r'\[(\w+)\]', prompt)
    if leftovers:
        unique_leftovers = sorted(set(leftovers))
        print(f"⚠️ WARNING: Template has {len(unique_leftovers)} unexpanded placeholders: {unique_leftovers}")
        print("   Use --vars to provide values for these variables")

    quality = template.get("quality", "high")
    aspect_ratio = template.get("aspect_ratio", "2:3")
    longest_side = template.get("longest side", "2048")

    if aspect_ratio == "2:3":
        w = int(int(longest_side) * 2 / 3)
        h = int(longest_side)
    elif aspect_ratio == "3:2":
        w = int(longest_side)
        h = int(int(longest_side) * 2 / 3)
    elif aspect_ratio == "9:16":
        w = int(int(longest_side) * 9 / 16)
        h = int(longest_side)
    elif aspect_ratio == "16:9":
        w = int(longest_side)
        h = int(int(longest_side) * 9 / 16)
    elif aspect_ratio == "1:1":
        w = h = int(longest_side)
    else:
        w = h = 1024

    w = ((w // 16) + 1) * 16 if w % 16 != 0 else w
    h = ((h // 16) + 1) * 16 if h % 16 != 0 else h
    size = f"{w}x{h}"
    return prompt, size, quality


TEMPLATE_NAME = "kpop-idol"

def build_prompt(template, variables, endpoint_provider=None):
    return default_template_to_prompt(template, variables, endpoint_provider)

#!/usr/bin/env python3
from __future__ import annotations
import re
import requests


def generate_dynamic_scenes(template, variables, endpoint_provider):
    girl_subject = variables.get("anime_girl_subject", "") or variables.get("girl_subject", "") or "动漫风格女性角色"
    man_subject = variables.get("man_subject", "") or "真实男性角色"
    background_scene = variables.get("background_scene", "") or "日常场景"
    mood_style = variables.get("mood_style", "") or "浪漫"
    theme = variables.get("theme", "")

    if variables.get("_user_provided_panels", False):
        print("  ✓ Using user-provided panel scenes")
        return variables

    endpoints = endpoint_provider()
    if not endpoints:
        print("Warning: No endpoints available for scene generation, using defaults")
        return variables

    endpoint = None
    for ep in endpoints:
        try:
            test_url = f"{ep['url']}/chat/completions"
            test_headers = {"Authorization": f"Bearer {ep['key']}", "Content-Type": "application/json"}
            test_resp = requests.post(test_url, headers=test_headers, json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 5,
            }, timeout=10)
            if test_resp.ok:
                endpoint = ep
                print(f"  Using {ep['name']} for scene generation")
                break
        except Exception:
            continue

    if not endpoint:
        print("Warning: No endpoint supports chat completions for scene generation")
        return variables

    prompt = f"""你是一位创意剧情设计师。根据以下角色和主题描述，为一张 3x3 海报设计 9 个不同的场景画面。

【男性角色】{man_subject}
【女性角色】{girl_subject}
【背景风格】{background_scene}
【整体氛围】{mood_style}
{f'【主题】{theme}' if theme else ''}

要求：
1. 每个场景必须和角色描述高度相关
2. 9 个场景必须互不相同
3. 每个场景用 10-20 个英文词描述
4. 输出格式：每行一个场景，以 "panel_X: " 开头
"""
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.9,
    }
    try:
        print("  Generating 9 dynamic scenes via LLM...")
        resp = requests.post(f"{endpoint['url']}/chat/completions", headers={
            "Authorization": f"Bearer {endpoint['key']}",
            "Content-Type": "application/json",
        }, json=payload, timeout=60)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        scene_mapping = {}
        for line in content.strip().split("\n"):
            match = re.match(r"^panel_?(\d+)[:\s]+(.+)$", line.strip(), re.IGNORECASE)
            if match:
                idx = int(match.group(1))
                scene = match.group(2).strip().strip('"').strip("'")
                if 1 <= idx <= 9:
                    scene_mapping[f"panel_{idx}"] = scene
        if len(scene_mapping) == 9:
            print("  ✓ 9 scenes generated successfully")
            variables.update(scene_mapping)
        else:
            print(f"  ⚠ Only got {len(scene_mapping)}/9 scenes, keeping defaults for missing")
            for i in range(1, 10):
                key = f"panel_{i}"
                if key in scene_mapping:
                    variables[key] = scene_mapping[key]
    except Exception as e:
        print(f"  ⚠ LLM scene generation failed: {e}, using defaults")
    return variables

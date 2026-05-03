#!/usr/bin/env python3
from __future__ import annotations


def replace_placeholders(text, variables):
    if not isinstance(text, str):
        return text
    for key, value in variables.items():
        text = text.replace(f"[{key}]", value)
    return text


def build_prompt(template, variables, endpoint_provider=None):
    variables = variables or {}

    # 主体
    subject = replace_placeholders(template["subject"]["描述"], variables)
    
    # 风格
    style = replace_placeholders(template["style"]["风格"], variables)
    features = ", ".join(replace_placeholders(x, variables) for x in template["style"]["特征"])
    
    # 模型/肌肤
    skin = replace_placeholders(template["model"]["肌肤"], variables)
    model_features = ", ".join(replace_placeholders(x, variables) for x in template["model"]["特征"])
    
    # 面部
    face = ", ".join(replace_placeholders(x, variables) for x in template["face"]["细节"])
    
    # 姿态
    pose = ", ".join(replace_placeholders(x, variables) for x in template["pose"]["姿态"])
    
    # 发型
    hair_desc = replace_placeholders(template["hair"]["描述"], variables)
    hair_features = ", ".join(replace_placeholders(x, variables) for x in template["hair"]["特征"])
    
    # 服装
    costume_desc = replace_placeholders(template["costume"]["描述"], variables)
    costume_features = ", ".join(replace_placeholders(x, variables) for x in template["costume"]["特征"])
    
    # 环境
    env_desc = replace_placeholders(template["environment"]["描述"], variables)
    env_features = ", ".join(replace_placeholders(x, variables) for x in template["environment"]["风格"])
    
    # 构图
    composition = ", ".join(replace_placeholders(x, variables) for x in template["composition"]["构图"])
    
    # 灯光
    lighting = ", ".join(replace_placeholders(x, variables) for x in template["lighting"]["灯光"])
    
    # 氛围
    mood = ", ".join(replace_placeholders(x, variables) for x in template["mood"]["氛围"])
    
    # 排版规则
    typography_rule = replace_placeholders(template["typography"]["排版规则"], variables)
    
    # 层级描述
    typography_levels = []
    for level in template["typography"]["层级"]:
        content = replace_placeholders(level["内容"], variables)
        font = level.get("字体", "")
        typography_levels.append(f"{content} ({font})")
    typography_levels_str = ". ".join(typography_levels)

    prompt = \
        f"{subject}. " \
        f"Style: {style}. Features: {features}. " \
        f"{skin}. {model_features}. " \
        f"Face: {face}. " \
        f"Pose: {pose}. " \
        f"{hair_desc}. {hair_features}. " \
        f"{costume_desc}. {costume_features}. " \
        f"Environment: {env_desc}. {env_features}. " \
        f"Composition: {composition}. " \
        f"Lighting: {lighting}. " \
        f"Mood: {mood}. " \
        f"Typography: {typography_rule}. {typography_levels_str}. " \
        f"masterpiece, best quality"

    quality = template.get("quality", "high")
    size = template.get("default_size")
    return prompt, size, quality
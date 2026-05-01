#!/usr/bin/env python3
"""
视频方案 Pitch Deck 生成器 - 3张图拆分方案

用法：
    python3 generate_pitchdeck.py --vars '{"title":"...","subtitle":"...",...}'
    
拆分规则：
    Panel 1: 角色设计 + 三视图 + 故事板分镜
             - 包含人物插画（唯一一张）
             - 禁止：色彩方案、物品道具、项目信息
    
    Panel 2: 项目信息 + 物品道具 + 抽象分镜 + 情感曲线
             - 禁止：人物插画、场景插画
             - 纯信息与图表展示
    
    Panel 3: 色彩方案 + 灯光 + 声音 + 参考画廊
             - 禁止：人物插画、场景插画
             - 纯技术设计展示
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent.resolve()
SKILL_DIR = TEMPLATE_DIR.parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
DEFAULT_OUTPUT_DIR = "~/.hermes/output/gpt-image-2"


def resolve_output_dir():
    """从 config.json 读取 output_dir，返回 video-pitch 模板子目录。"""
    import json
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    except Exception:
        config = {}
    base = Path(config.get('output_dir', DEFAULT_OUTPUT_DIR)).expanduser()
    return base / "video-pitch"


def build_panel_1_prompt(vars_dict):
    """构建 Panel 1 的 prompt（角色 + 故事板）- 美观排版版"""
    
    title = vars_dict.get("title", "UNTITLED")
    subtitle = vars_dict.get("subtitle", "")
    
    # 女主信息
    female_char = vars_dict.get("female_char", "")
    female_age = vars_dict.get("female_age", "")
    female_role = vars_dict.get("female_role", "")
    female_appearance = vars_dict.get("female_appearance", "")
    female_keywords = vars_dict.get("female_keywords", "")
    female_costume = vars_dict.get("female_costume", "")
    female_turnaround = vars_dict.get("female_turnaround", "")
    
    # 男主信息
    male_char = vars_dict.get("male_char", "")
    male_age = vars_dict.get("male_age", "")
    male_role = vars_dict.get("male_role", "")
    male_appearance = vars_dict.get("male_appearance", "")
    male_keywords = vars_dict.get("male_keywords", "")
    male_costume = vars_dict.get("male_costume", "")
    male_turnaround = vars_dict.get("male_turnaround", "")
    
    # 故事板
    story_flow = vars_dict.get("story_flow", "")
    key_dialogue = vars_dict.get("key_dialogue", "")
    
    prompt = f"""Pitch Deck Page 1 - CHARACTER DESIGN & STORYBOARD

========================================
    {title}
    {subtitle}
========================================

╔══════════════════════════════════════╗
║         FEMALE LEAD DESIGN           ║
║    CHARACTER NAME: {female_char}      ║
╚══════════════════════════════════════╝

**IMPORTANT: Use this exact character name: {female_char}**
Name: {female_char}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Age: {female_age}  • Role: {female_role}
• Appearance: {female_appearance}
• Keywords: {female_keywords}
• Costume: {female_costume}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【TURNAROUND REFERENCE】
{female_turnaround}

╔══════════════════════════════════════╗
║          MALE LEAD DESIGN            ║
║    CHARACTER NAME: {male_char}        ║
╚══════════════════════════════════════╝

**IMPORTANT: Use this exact character name: {male_char}**
Name: {male_char}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Age: {male_age}  • Role: {male_role}
• Appearance: {male_appearance}
• Keywords: {male_keywords}
• Costume: {male_costume}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【TURNAROUND REFERENCE】
{male_turnaround}

╔══════════════════════════════════════╗
║          STORYBOARD PANELS           ║
╚══════════════════════════════════════╝

**Storyboard must use character names: {female_char} and {male_char}**
{story_flow}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【KEY DIALOGUE】
{key_dialogue}

========================================

CHARACTER NAME CONSTRAINTS:
- Female character MUST be labeled as: {female_char}
- Male character MUST be labeled as: {male_char}
- Do NOT invent new names
- Use exact character names in all storyboard labels and dialogue

LAYOUT REQUIREMENTS:
• Elegant grid layout with clear visual hierarchy
• Character turnarounds displayed as elegant reference strips
• Storyboard panels arranged in clean sequential grid (2x4 or 3x3)
• Use decorative borders and section dividers
• Balanced spacing between elements
• Professional magazine-quality composition
• Dark background with gold/cream accents
• NO color palette swatches
• NO props illustrations
• NO project info section

Style: High-end fashion magazine layout, character design sheet aesthetic, elegant typography, premium pitch deck presentation, beautiful balanced composition"""
    
    return prompt


def build_panel_2_prompt(vars_dict):
    """构建 Panel 2 的 prompt（项目 + 道具插画 + 抽象分镜 + 情感）"""
    
    title = vars_dict.get("title", "UNTITLED")
    subtitle = vars_dict.get("subtitle", "")
    
    # 项目信息
    video_type = vars_dict.get("video_type", "")
    duration = vars_dict.get("duration", "")
    genre = vars_dict.get("genre", "")
    target_audience = vars_dict.get("target_audience", "")
    
    # 故事
    one_line_synopsis = vars_dict.get("one_line_synopsis", "")
    core_conflict = vars_dict.get("core_conflict", "")
    emotional_arc = vars_dict.get("emotional_arc", "")
    
    # 环境设定
    core_scene = vars_dict.get("core_scene", "")
    scene_mood = vars_dict.get("scene_mood", "")
    time_of_day = vars_dict.get("time_of_day", "")
    season = vars_dict.get("season", "")
    weather = vars_dict.get("weather", "")
    weather_effect = vars_dict.get("weather_effect", "")
    
    # 物品道具
    key_props = vars_dict.get("key_props", "")
    
    # 运镜与节奏
    camera_style = vars_dict.get("camera_style", "")
    key_shot_types = vars_dict.get("key_shot_types", "")
    transition_style = vars_dict.get("transition_style", "")
    overall_pacing = vars_dict.get("overall_pacing", "")
    emotional_peak = vars_dict.get("emotional_peak", "")
    opening_style = vars_dict.get("opening_style", "")
    ending_style = vars_dict.get("ending_style", "")
    
    prompt = f"""Pitch Deck Page 2 - PROJECT INFO & PROPS & VISUAL STRUCTURE

========================================
    {title} | Project Overview
========================================

╔══════════════════════════════════════╗
║           PROJECT INFO               ║
╚══════════════════════════════════════╝

• Type: {video_type}  • Duration: {duration}
• Genre: {genre}  • Target: {target_audience}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【SYNOPSIS】
{one_line_synopsis}

【CONFLICT】
{core_conflict}

【EMOTIONAL ARC】
{emotional_arc}

╔══════════════════════════════════════╗
║        ENVIRONMENT SETTINGS          ║
╚══════════════════════════════════════╝

Scene: {core_scene}
Mood: {scene_mood}
Time: {time_of_day}
Season: {season} | Weather: {weather}
Special Effect: {weather_effect}

╔══════════════════════════════════════╗
║        KEY PROPS ILLUSTRATION        ║
╚══════════════════════════════════════╝

Items: {key_props}

【PROP VISUAL REFERENCE】
Show beautiful isolated prop illustrations:
- Clean product-style renderings of each prop
- Elegant composition with props floating/arranged aesthetically
- Detailed material and texture rendering
- NO hands holding props, NO figures
- Props as standalone design elements

╔══════════════════════════════════════╗
║       VISUAL STRUCTURE DIAGRAM       ║
╚══════════════════════════════════════╝

Phase 1: Opening → {opening_style}
Phase 2: Build-up → Rising tension
Phase 3: Peak → {emotional_peak}
Phase 4: Resolution → {ending_style}

【PACING CURVE】
{overall_pacing}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【CAMERA STYLE】
Style: {camera_style}
Shots: {key_shot_types}
Transitions: {transition_style}

========================================

LAYOUT REQUIREMENTS:
• Beautiful prop illustrations section (isolated, no characters)
• Visual flow diagram with elegant arrows and stages
• Emotional curve as beautiful wave/sine visualization
• Camera style illustrated as abstract lens diagrams
• Balanced grid layout with visual interest
• Decorative icons and abstract symbols
• Dark background with gold accents

CONSTRAINTS:
• NO character illustrations (human figures)
• NO scene backgrounds (environments, locations)
• Props shown as isolated design elements only
• Can include: diagrams, charts, icons, symbols, abstract graphics

Style: Professional pitch deck, product design aesthetic, elegant information design, visual hierarchy, beautiful composition with prop illustrations"""
    
    return prompt


def build_panel_3_prompt(vars_dict):
    """构建 Panel 3 的 prompt（色彩 + 灯光 + 声音）"""
    
    title = vars_dict.get("title", "UNTITLED")
    subtitle = vars_dict.get("subtitle", "")
    
    # 色彩
    color1_name = vars_dict.get("color1_name", "")
    color1_hex = vars_dict.get("color1_hex", "")
    color1_use = vars_dict.get("color1_use", "")
    color2_name = vars_dict.get("color2_name", "")
    color2_hex = vars_dict.get("color2_hex", "")
    color2_use = vars_dict.get("color2_use", "")
    color3_name = vars_dict.get("color3_name", "")
    color3_hex = vars_dict.get("color3_hex", "")
    color3_use = vars_dict.get("color3_use", "")
    color4_name = vars_dict.get("color4_name", "")
    color4_hex = vars_dict.get("color4_hex", "")
    color4_use = vars_dict.get("color4_use", "")
    color_mood = vars_dict.get("color_mood", "")
    
    # 灯光
    lighting_style = vars_dict.get("lighting_style", "")
    light_feature1 = vars_dict.get("light_feature1", "")
    light_feature2 = vars_dict.get("light_feature2", "")
    light_feature3 = vars_dict.get("light_feature3", "")
    
    # 声音
    music_genre = vars_dict.get("music_genre", "")
    ambient_sound = vars_dict.get("ambient_sound", "")
    key_sound_effects = vars_dict.get("key_sound_effects", "")
    
    # 参考
    ref1 = vars_dict.get("ref1", "")
    ref2 = vars_dict.get("ref2", "")
    ref3 = vars_dict.get("ref3", "")
    ref4 = vars_dict.get("ref4", "")
    
    prompt = f"""Pitch Deck Page 3 - COLOR, LIGHTING & AUDIO DESIGN

Title: {title} | 色彩与氛围设计

=== COLOR PALETTE ===
Color 1: {color1_name} {color1_hex} - {color1_use}
Color 2: {color2_name} {color2_hex} - {color2_use}
Color 3: {color3_name} {color3_hex} - {color3_use}
Color 4: {color4_name} {color4_hex} - {color4_use}

Overall Mood: {color_mood}

=== LIGHTING DESIGN ===
Style: {lighting_style}
Features: {light_feature1}, {light_feature2}, {light_feature3}

=== AUDIO DESIGN ===
Music: {music_genre}
Ambient Sound: {ambient_sound}
Key SFX: {key_sound_effects}

=== VISUAL REFERENCES ===
- {ref1}
- {ref2}
- {ref3}
- {ref4}

IMPORTANT CONSTRAINTS:
- NO character illustrations or drawings
- NO scene illustrations or backgrounds
- NO human figures
- NO environment art
- ONLY color swatches, lighting diagrams, audio design panels
- References as text descriptions or abstract mood indicators

Style: Professional pitch deck, color swatches layout, lighting mood board, audio design panel, dark background, gold typography, NO characters, NO scenes"""
    
    return prompt


def generate_panel(prompt, output_name, size="1440x2560", timeout=500):
    """调用 generate.py 生成单张图片"""
    
    cmd = [
        "python3",
        str(SKILL_DIR / "generate.py"),
        "--template", "video-pitch",  # 添加模板参数，让 history 保存到模板目录
        "--prompt", prompt,
        "--size", size,
        "--quality", "high",
        "--output", output_name,
        "--timeout", str(timeout)
    ]
    
    print(f"Generating: {output_name}")
    result = subprocess.run(cmd, cwd=str(SKILL_DIR), capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    
    print(f"Success: {output_name}")
    return True


def combine_panels(prefix, labels, timeout=500):
    """拼接3张图片"""
    
    cmd = [
        "python3",
        str(Path(__file__).parent / "combine_panels.py"),
        "--images", f"{prefix}-panel-1.png,{prefix}-panel-2.png,{prefix}-panel-3.png",
        "--layout", "vertical",
        "--labels", labels,
        "--output", f"{prefix}-full-pitchdeck.png"
    ]
    
    print(f"Combining panels...")
    result = subprocess.run(cmd, cwd=str(SKILL_DIR), capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    
    print(f"Combined: {prefix}-full-pitchdeck.png")
    return resolve_output_dir() / f"{prefix}-full-pitchdeck.png"


def main():
    parser = argparse.ArgumentParser(
        description="video-pitch / generate_pitchdeck：生成多 panel pitch deck（history 在模板目录，图片 output 在 ~/.hermes/output/gpt-image-2/video-pitch/）"
    )
    parser.add_argument("--vars", type=str, required=True, help="变量JSON字符串")
    parser.add_argument("--prefix", type=str, default="pitch", help="输出文件前缀")
    parser.add_argument("--size", type=str, default="1440x2560", help="单张图片尺寸")
    parser.add_argument("--timeout", type=int, default=500, help="传递给 generate.py 的超时秒数")
    parser.add_argument("--no-combine", action="store_true", help="不拼接图片")
    
    args = parser.parse_args()
    
    # 解析变量
    try:
        vars_dict = json.loads(args.vars)
    except json.JSONDecodeError as e:
        print(f"Error parsing vars JSON: {e}")
        sys.exit(1)
    
    # 生成 Panel 1
    prompt1 = build_panel_1_prompt(vars_dict)
    if not generate_panel(prompt1, f"{args.prefix}-panel-1.png", args.size, args.timeout):
        sys.exit(1)
    
    # 生成 Panel 2
    prompt2 = build_panel_2_prompt(vars_dict)
    if not generate_panel(prompt2, f"{args.prefix}-panel-2.png", args.size, args.timeout):
        sys.exit(1)
    
    # 生成 Panel 3
    prompt3 = build_panel_3_prompt(vars_dict)
    if not generate_panel(prompt3, f"{args.prefix}-panel-3.png", args.size, args.timeout):
        sys.exit(1)
    
    # 拼接
    if not args.no_combine:
        labels = "Page 1: 角色设计+故事板,Page 2: 项目+抽象分镜+情感,Page 3: 色彩+灯光+声音"
        combine_panels(args.prefix, labels, args.timeout)
    
    print("\nDone! Generated files:")
    print(f"  - {args.prefix}-panel-1.png (角色 + 故事板)")
    print(f"  - {args.prefix}-panel-2.png (项目 + 抽象分镜)")
    print(f"  - {args.prefix}-panel-3.png (色彩 + 灯光 + 声音)")
    if not args.no_combine:
        print(f"  - {args.prefix}-full-pitchdeck.png (拼接版)")


if __name__ == "__main__":
    main()
---
name: gpt-image-2
description: 使用 GPT-Image-2 API 生成高质量图片，支持文生图、图生图、局部编辑、多图合成、模板生成等能力
version: 5.2.0
author: _wysl
tags:
  - image
  - generation
  - gpt-image
  - photorealism
  - edit
  - virtual-try-on
  - template
---

# GPT-Image-2 Skill

使用 `router-daoge-me` provider 下的 `gpt-image-2` API 生成图片。

## 主要入口

```text
/root/.openclaw/skills/gpt-image-2/generate.py                     # 通用入口（底层 API / 非模板）

# 模板目录化入口（推荐且唯一保留）
/root/.openclaw/skills/gpt-image-2/template/poster-cosplay/run.py
/root/.openclaw/skills/gpt-image-2/template/video-pitch/run.py
/root/.openclaw/skills/gpt-image-2/template/video-pitch/generate_pitchdeck.py
/root/.openclaw/skills/gpt-image-2/template/video-pitch/combine_panels.py
/root/.openclaw/skills/gpt-image-2/template/portrait-photography/run.py
/root/.openclaw/skills/gpt-image-2/template/couple-portrait/run.py
/root/.openclaw/skills/gpt-image-2/template/kpop-idol/run.py
/root/.openclaw/skills/gpt-image-2/template/street-photography/run.py
/root/.openclaw/skills/gpt-image-2/template/bedroom-mirror-selfie/run.py
/root/.openclaw/skills/gpt-image-2/template/person-photoshoot-3x3/run.py
/root/.openclaw/skills/gpt-image-2/template/anime-girl-and-man-date-photo-collage-3x3/run.py
```

## 模板与脚本的关系

现在每个模板都放到自己的子目录下：

```text
template/<template-name>/
├── template.json     # 该模板自己的 JSON 定义
├── builder.py        # 该模板自己的 prompt builder
└── run.py            # 该模板自己的固定入口
```

其中 `video-pitch` 额外包含：

```text
template/video-pitch/
├── generate_pitchdeck.py   # 多 panel pitch deck 生成
└── combine_panels.py       # 多图拼接 / panel 合成
```

| 模板名 | 目录 | 入口脚本 | 说明 |
|---|---|---|---|
| `poster-cosplay` | `template/poster-cosplay/` | `run.py` | Cosplay 海报 |
| `video-pitch` | `template/video-pitch/` | `run.py` | 视频提案模板；额外含 pitchdeck / combine_panels |
| `portrait-photography` | `template/portrait-photography/` | `run.py` | 人像摄影 |
| `couple-portrait` | `template/couple-portrait/` | `run.py` | 双人写真 |
| `kpop-idol` | `template/kpop-idol/` | `run.py` | 韩流偶像 |
| `street-photography` | `template/street-photography/` | `run.py` | 街头摄影 |
| `bedroom-mirror-selfie` | `template/bedroom-mirror-selfie/` | `run.py` | 卧室镜前自拍 |
| `person-photoshoot-3x3` | `template/person-photoshoot-3x3/` | `run.py` | 人物写真 3x3 |
| `anime-girl-and-man-date-photo-collage-3x3` | `template/anime-girl-and-man-date-photo-collage-3x3/` | `run.py` | 二次元少女与男生约会拼贴 3x3 |

设计意图：
- **模板、builder、入口脚本放在一起**，改某个模板时不影响其他模板
- `generate.py` 只保留通用层：API 调用、history、尺寸校验、fallback、通用 CLI
- `generate_pitchdeck.py` / `combine_panels.py` 归到 `video-pitch` 目录，语义上更清楚
- **不再依赖单独的 `template_scripts/` 目录**，模板实现彻底收口到各自子目录内

## History / Output 规则

- **通用 prompt** 生成的 history：`/root/.openclaw/skills/gpt-image-2/history/`
- **模板生成** 的 history：`/root/.openclaw/skills/gpt-image-2/template/<template-name>/history/`
- **所有图片 output**（无论模板还是通用 prompt）：统一落在 ` /root/.openclaw/skills/gpt-image-2/output/ `

也就是：
- **history 按模板分流**
- **output 保持在 skill 根目录统一管理**

## 配置

配置文件：`/root/.openclaw/skills/gpt-image-2/config.json`

- 支持多 endpoint fallback
- 按 `priority` 顺序重试
- 每个 endpoint 重试次数由 `retry_count` 控制
- 当前仅支持模型：`gpt-image-2`

## 常用参数

| 参数 | 说明 |
|------|------|
| `--prompt` | 图片描述，支持中文 |
| `--template` | 模板名称 |
| `--vars` | 模板变量 JSON |
| `--size` | 输出分辨率，默认 `1024x1536` |
| `--output` | 输出文件名 |
| `--image` | 参考图路径 |
| `--mask` | 蒙版路径 |
| `--mode` | `generate` / `edit` / `composite` / `inpaint` |
| `--timeout` | 请求超时秒数，默认 `500` |
| `--list-templates` | 列出全部模板 |

## 模板

补充说明见：`docs/basic.md`、`docs/advanced.md`

当前可用模板：

- `poster-cosplay`（中文名：Cosplay 海报）
- `video-pitch`（中文名：视频提案）
- `portrait-photography`（中文名：人像摄影）
- `couple-portrait`（中文名：双人写真）
- `kpop-idol`（中文名：韩流偶像）
- `street-photography`（中文名：街头摄影）
- `bedroom-mirror-selfie`（中文名：卧室镜前自拍）
- `person-photoshoot-3x3`（中文名：人物写真3x3）
- `anime-girl-and-man-date-photo-collage-3x3`（中文名：二次元少女与男生约会拼贴3x3）
  - 约束：男角色强制真人化（live-action），女角色强制二次元/动漫化（anime / 2D illustrated）

## 分辨率约束

- 最大边长 `<= 3840px`
- 宽高必须为 `16` 的倍数
- 长短边比例 `≤ 3:1`
- 总像素范围：`655,360 ~ 8,294,400`
- 超过 `2560x1440` 视为实验性

常用尺寸：

- `1024x1024`
- `1536x1024`
- `1024x1536`
- `2560x1440`
- `1440x2560`
- `2160*3840`

## Prompt 建议

建议按这个顺序组织：

```text
场景/背景 → 主体 → 关键细节 → 约束条件
```

常用约束词：

- `no watermark`
- `no extra text`
- `no logos`
- `keep everything else the same`
- `change only X`

## 常用示例

### 1. 文生图

```bash
python3 generate.py --prompt "A photorealistic portrait..." --size 1024x1536 --output test.png
```

### 2. 模板生成

```bash
python3 template/poster-cosplay/run.py --vars '{"xxx":"角色名"}' --output poster.png --timeout 500
```

### 2.1 人物写真3x3 模板示例

```bash
cd template/person-photoshoot-3x3
python3 run.py \
  --vars '{
    "subject_name":"Kim Minji",
    "outfit_style":"white oversized shirt + black shorts, same outfit across all frames",
    "title_text":"Kim Minji 3x3",
    "tagline_text":"100% 一致性"
  }' \
  --output person-photoshoot-3x3.png \
  --timeout 500
```

### 2.2 二次元少女与男生约会拼贴3x3 模板示例

```bash
cd template/anime-girl-and-man-date-photo-collage-3x3
python3 run.py \
  --vars '{
    "title_text":"Anime Girl and Man Date Photo Collage 3x3",
    "subtitle_text":"二次元少女与男生约会拼贴3x3",
    "tagline_text":"100% 一致性",
    "required_keyword":"100% 一致性",
    "mood_style":"intimate candid couple energy"
  }' \
  --output anime-date-3x3.png \
  --timeout 500
```

### 2.3 `person-photoshoot-3x3` 常用 vars

- `required_keyword`：强制关键词，默认建议始终保持 `100% 一致性`
- `subject_name`：人物名
- `subject_type`：人物类型
- `series_style`：系列风格
- `poster_style`：海报风格
- `aesthetic_style`：审美关键词
- `tone_style`：整体气质
- `makeup_style`：妆容
- `skin_texture`：皮肤质感
- `expression_style`：表情倾向
- `hair_style`：发型
- `outfit_style`：服装
- `background_scene`：场景
- `lighting_style`：灯光
- `title_text`：主标题
- `subtitle_text`：副标题
- `tagline_text`：短标语
- `mood_style`：氛围
- `top_left_pose` / `top_center_pose` / `top_right_pose`
- `mid_left_pose` / `mid_center_pose` / `mid_right_pose`
- `bottom_left_pose` / `bottom_center_pose` / `bottom_right_pose`

### 2.4 `anime-girl-and-man-date-photo-collage-3x3` 常用 vars

- `required_keyword`：强制关键词，默认建议始终保持 `100% 一致性`
- `title_text`：主标题
- `subtitle_text`：副标题
- `tagline_text`：短标语
- `poster_style`：整体海报风格
- `man_subject`：真人男性主体描述
- `anime_girl_subject`：二次元少女主体描述
- `background_scene`：整体场景基调
- `lighting_style`：灯光风格
- `mood_style`：氛围
- `panel_1` ~ `panel_9`：9 个拼贴分镜内容

> ⚠️ **3x3 剧情场景自动生成**
> 使用 `anime-girl-3x3` 或 `person-photoshoot-3x3` 模板时，系统会自动调用 LLM 根据角色描述和主题
> 生成 9 个不同的剧情场景。每次运行都会产生不同的场景组合，避免雷同。
> 如果通过 `--vars` 传入了 `panel_1` ~ `panel_9`，则跳过自动生成，使用用户自定义场景。

### 3. 图片编辑

```bash
python3 generate.py --mode edit --image photo.png --mask mask.png --prompt "Change only the dress, keep everything else the same" --output edited.png
```

### 4. 多图合成

```bash
python3 generate.py --mode composite --image person.png,clothing.png --prompt "Apply the clothing from Image 2 to Image 1" --output result.png
```

### 5. Pitch Deck 生成

```bash
python3 template/video-pitch/generate_pitchdeck.py --prefix myproject --vars '{"title":"PROJECT TITLE"}'
```

> ⚠️ 注：`template/video-pitch/generate_pitchdeck.py` 仅支持 `--vars` 参数，不支持 `--template`。所有变量必须通过 `--vars` 传入。

输出文件：

- `{prefix}-panel-1.png`
- `{prefix}-panel-2.png`
- `{prefix}-panel-3.png`
- `{prefix}-full-pitchdeck.png`

### 6. 多图拼接

```bash
python3 template/video-pitch/combine_panels.py --images img1.png,img2.png,img3.png --layout vertical --output combined.png
```

支持布局：`vertical` / `horizontal` / `grid`

## 调用注意事项

1. API 返回 base64，不返回 URL
2. 中文 prompt 可直接使用
3. 编辑时尽量写清楚 `change only X` / `keep everything else the same`
4. 多图输入时建议在 prompt 中明确写 `Image 1`、`Image 2`
5. 图片生成可能较慢，可直接运行脚本并给予足够外层执行时间
6. **输出流程：先展示 prompt，再执行生成，再发送图片结果**
7. **统一建议**：skill 内所有生成相关调用默认显式传 `--timeout 500`

推荐调用方式：

```bash
python3 generate.py --prompt '...' --output test.png --timeout 500
```

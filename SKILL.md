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
~/.hermes/skills/gpt-image-2/generate.py                     # 通用入口（底层 API / 非模板）

# 模板目录化入口（推荐且唯一保留）
~/.hermes/skills/gpt-image-2/template/poster-cosplay/run.py
~/.hermes/skills/gpt-image-2/template/video-pitch/run.py
~/.hermes/skills/gpt-image-2/template/video-pitch/generate_pitchdeck.py
~/.hermes/skills/gpt-image-2/template/video-pitch/combine_panels.py
~/.hermes/skills/gpt-image-2/template/portrait-photography/run.py
~/.hermes/skills/gpt-image-2/template/couple-portrait/run.py
~/.hermes/skills/gpt-image-2/template/kpop-idol/run.py
~/.hermes/skills/gpt-image-2/template/street-photography/run.py
~/.hermes/skills/gpt-image-2/template/bedroom-mirror-selfie/run.py
~/.hermes/skills/gpt-image-2/template/person-photoshoot-3x3/run.py
~/.hermes/skills/gpt-image-2/template/anime-girl-and-man-date-photo-collage-3x3/run.py
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

- **通用 prompt** 生成的 history：`history/`（skill 目录内）
- **模板生成** 的 history：`template/<template-name>/history/`
- **通用 prompt 生成的图片 output**：`~/.hermes/output/gpt-image-2/normal/`
- **模板生成的图片 output**：`~/.hermes/output/gpt-image-2/<template-name>/`
- output 目录可在 `config.json` 的 `output_dir` 字段中自定义，也支持 `~` 开头的路径或相对路径

**配置示例（config.json）：**
```json
{
  "output_dir": "/your/custom/output/path"
}
```

也就是：
- **history 按模板分流**（在 skill 目录内）
- **output 也按模板分流**（在统一的 output 目录下，可通过 `output_dir` 迁移到任意位置）

## 配置

配置文件：`~/.hermes/skills/gpt-image-2/config.json`

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

## 模板兼容策略（重要）

当上游任务（如 Feishu / 其他 agent / 外部工作流）提供的角色、服装、场景细节 **多于模板原生占位符数量** 时：

**不要直接丢信息，也不要优先修改模板文件。**
优先采用 **调用层兼容**：
- 保持模板目录下 `template.json` / `builder.py` / `run.py` 不变
- 分析模板现有占位符与默认结构
- 将上游细节 **压缩、映射、折叠** 到模板可承载的字段中
- 仍然通过模板入口执行，而不是绕开模板直接改成通用 prompt（除非任务明确不要求模板）

核心原则：
1. **模板不动，调用兼容**
2. **细节不够放时，压缩后塞入最相关字段，不要舍弃核心视觉元素**
3. **优先保留“看得见”的信息**：角色身份、核心服装、材质/剪裁、发型、配饰、手持物、场景锚点、风格词
4. **弱化抽象说明词**：人设解释、背景故事、情绪推导等，在字段容量不足时优先让位给视觉信息
5. **避免把一个模板的调用习惯误套到另一个模板**；先看 `template.json` 中真实存在的占位符再组织 vars

### 通用兼容工作流

1. 读取目标模板的 `template.json`
2. 找出真实占位符（如 `[xxx]`、`[model_clothing]`、`[background_type]`）
3. 判断上游信息是否“字段过载”
4. 采用以下之一：
   - **直接映射**：上游字段可以一一填进模板 vars
   - **单字段压缩**：多个细节压成一个高信息密度字符串，塞进单一入口
   - **相关字段拆分**：把服装、发型、场景分别压进最接近的几个字段
5. 生成前自查：是否丢了核心视觉元素

---

## 各模板兼容建议

### 1) `poster-cosplay`

**特征：** 单入口模板，核心占位符基本只有 `[xxx]`

**风险：** 上游细节一多，最容易被错误简化成泛化 prompt

**注意：** 此模板默认生成杂志封面风格，会自动添加标题、副标题、条形码、定价等文字元素。如果需要纯净无文字图片， workflow 为：
```bash
# Step 1: 用模板生成
python3 template/poster-cosplay/run.py --vars '{"xxx":"..."}' --output img.png --timeout 500

# Step 2: 用 edit 模式去除文字
python3 generate.py --mode edit --image img.png \
  --prompt "Remove all text overlays, magazine titles, subtitles, barcodes, price, and any text from this image. Keep the main character and background exactly the same." \
  --output img_no_text.png --timeout 500
```

**兼容策略：**
- 不改模板文件
- 将上游关键信息压缩为一个 `xxx` 字符串
- `xxx` 推荐优先级：
  1. 角色 / IP
  2. 核心服装（颜色、材质、关键剪裁）
  3. 发型
  4. 头饰 / 耳环 / 手持物
  5. 场景锚点
  6. 风格词（cosplay / 真实感 / 高还原度）

**推荐格式：**
```text
<角色/IP>，<核心服装>，<关键材质/剪裁>，<发型>，<配饰>，<手持物>，<场景锚点>，<风格>
```

**示例：**
```bash
python3 template/poster-cosplay/run.py \
  --vars '{"xxx":"碧蓝航线大凤，红色修身晚礼服配黑丝，蓬松裙摆，蕾丝花边与珠片刺绣，优雅盘发，钻石发饰，珍珠耳环，手持红玫瑰，留声机氛围，真实感高还原度 cosplay"}' \
  --output taihou_cosplay.png \
  --timeout 500
```

### 2) `portrait-photography`

**特征：** 占位符较细，适合真人摄影类定向描述

**可映射字段：**
- `model_name`：角色/主体名
- `model_appearance`：脸、体态、年龄感、种族风格等
- `model_clothing`：服装主体 + 材质 + 剪裁 + 配件主信息
- `model_makeup`：妆容 + 耳饰/面部配件
- `model_hair`：发型 + 发色 + 发饰
- `background_type`：场景与布景锚点
- `lighting_type` / `mood_type` / `pose_angle`：补充摄影表达

**兼容策略：**
- 优先走多字段直接映射
- 若上游服装信息过长，把“服装本体 + 最重要配件”留在 `model_clothing`
- 将“发饰”优先放 `model_hair`，将“耳环/面部饰品”优先放 `model_makeup`

### 3) `person-photoshoot-3x3`

**特征：** 多字段 + 九宫格动作位；适合同一人物一致性表达

**兼容策略：**
- `subject_name` / `subject_type`：角色身份
- `hair_style` / `outfit_style` / `makeup_style`：承接主体视觉信息
- `background_scene` / `lighting_style` / `mood_style`：承接场景与氛围
- 若上游只有“角色设定”没有 9 个动作：
  - 先保住一致性相关字段
  - 再补 9 个动作位，动作可由主题自然展开，但不能改掉主体服装与发型
- 当字段过载时，**优先保证人物一致性 > 服装一致性 > 动作丰富度**

### 4) `couple-portrait`

**特征：** 双人模板，字段分 person A / person B

**兼容策略：**
- 先拆角色信息，不要把两个人的信息混成一个长串
- `person_a_*` / `person_b_*` 分别承接外观与服装
- `interaction_type` 承接互动关系
- `background_scene` 承接共同场景
- 若上游一方信息明显更少，不要硬编太多细节；优先保主体方

### 5) `kpop-idol`

**特征：** 偶像概念照模板，强调概念、造型、色系

**兼容策略：**
- `idol_concept`：主题概念
- `idol_costume`：服装主体
- `idol_makeup_hair`：妆发 + 饰品压缩写入
- `color_theme` / `background_type`：颜色与舞台/概念布景
- 若上游提供很多服装细节，优先保留可见度最高的 3~5 个点

### 6) `street-photography`

**特征：** 字段非常多，偏摄影纪实表达

**兼容策略：**
- 先抽“主体 / 地点 / 时段 / 天气 / 光线 / 情绪 / 瞬间动作”
- 不要把角色设定长段直接硬塞全部字段
- 优先填：`main_subject`、`subject_type`、`subject_pose`、`street_location`、`city_name`、`time_of_day`、`weather`、`lighting_condition`、`mood`
- 其余镜头参数不足时可用模板默认值，不必强造

### 7) `bedroom-mirror-selfie`

**特征：** 生活化单人模板，强调镜前自拍与卧室场景

**兼容策略：**
- `clothing_description`：服装主体
- `hair_description` / `face_features` / `expression`：人物视觉焦点
- `bedroom_description`：卧室锚点
- `pose_description`：自拍动作
- 若上游含大量场景杂项，只保留与镜前自拍相关的可见信息

### 8) `anime-girl-and-man-date-photo-collage-3x3`

**特征：** 双主体 + 九宫格剧情

**兼容策略：**
- `anime_girl_subject` 和 `man_subject` 分开压缩
- `background_scene` / `lighting_style` / `mood_style` 控整体调性
- 如上游剧情不足：优先保角色外观一致性，再让 panel 自动展开
- 如上游已给定关键互动桥段，应优先手填 `panel_1` ~ `panel_9`

### 9) `video-pitch`

**特征：** 信息密度很高，偏提案板 / 影视策划

**兼容策略：**
- 先按“人物 / 场景 / 色彩 / 运镜 / 情绪 / 音效”分类
- 避免把全部信息堆进 `one_line_synopsis`
- 上游信息不足时，优先保证：`title`、`one_line_synopsis`、`core_scene`、`story_flow`、`visual_style`、`lighting_style`、`color_mood`

---

## 执行提醒

- **先分析模板真实占位符，再决定兼容方式**
- **不要因为模板字段少就擅自改成另一个模板**；除非用户明确同意
- **不要因为模板字段少就舍弃细节**；应压缩后映射
- **优先模板兼容，次选通用 prompt**；只有任务明确不要求模板时，才绕开模板
- 若同类兼容需求持续出现，再考虑新增“调用层映射脚本”，但默认先人工兼容

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

## 平台兼容性

**MEDIA: 发送支持情况：**
- ✅ 支持：telegram, discord, matrix, weixin, signal, yuanbao
- ❌ 不支持：feishu（飞书）

**飞书平台限制：**
- 无法通过 MEDIA: 发送文件
- 大图片（10MB+）可能显示异常
- 替代方案：用 markdown 路径展示、压缩图片、或提供文件路径让用户自行获取

推荐调用方式：

```bash
python3 generate.py --prompt '...' --output test.png --timeout 500
```

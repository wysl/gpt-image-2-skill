# 基础用法

本文档补充 `README.md` 中的通用用法，重点说明怎样写更稳定的 prompt，以及什么时候该用通用入口而不是模板。

## 何时使用 `generate.py`

优先使用 `generate.py` 的场景：

- 你已经有完整 prompt，不需要模板变量。
- 你在做一次性的概念图、示意图、信息图或广告图。
- 你需要 `edit`、`composite` 或 `inpaint` 模式。

基础命令：

```bash
python3 generate.py --prompt "your prompt" --size 1024x1536 --quality high
```

如果不传 `--size`，通用生成会默认读取当前最高优先级 endpoint 的 `design_max_size`。

## Prompt 编写建议

### 1. 信息图

适合：流程图、结构图、时间线、说明图。

建议：

- 明确主题和信息流顺序。
- 元素较多时使用结构化描述。
- 文字密集时保持 `quality high`。

示例：

```text
Create a detailed infographic about the workflow of an automatic coffee machine.
Show the flow from bean storage to grinding, weighing, water heating, extraction, and cup output.
Use a clean layout with clear labels and a professional design style.
```

### 2. 写实摄影

适合：人物肖像、产品摄影、写实场景。

建议：

- 使用镜头、光线、构图和材质语言。
- 明确真实纹理，而不是只写“高清”“精美”。
- 需要细节时写清楚皮肤、材质、环境状态。

示例：

```text
Create a photorealistic candid portrait of an elderly sailor on a fishing boat.
Weathered skin, visible wrinkles and pores, salt-stained clothing, soft coastal daylight, shallow depth of field, subtle film grain.
The image should feel honest and unposed, with no heavy retouching.
```

### 3. Logo

适合：简洁品牌标志探索。

建议：

- 说明品牌性格和使用场景。
- 强调简洁、可缩放、非侵权。
- 避免把大量品牌故事直接塞进 prompt。

示例：

```text
Create an original, non-infringing logo for a local bakery called Field & Flour.
The logo should feel warm, simple, and timeless.
Use clean vector-like shapes, strong silhouette, balanced negative space, and a plain background.
```

### 4. 广告图

适合：品牌广告、活动 KV、营销海报。

建议：

- 像写简短创意简报，而不是堆参数。
- 明确品牌、受众、场景和文案。
- 如果需要画面里出现文字，用引号包住并说明“清晰可读”。

示例：

```text
Create a polished campaign image for a youth streetwear brand called Thread.
Show a group of friends in an urban setting with the tagline "Yours to Create" rendered exactly once.
Use clean composition, strong color direction, natural poses, and no extra text or watermarks.
```

### 5. 多格漫画或分镜

适合：短故事、概念分镜、多格图。

建议：

- 一格写一个明确动作或情节。
- 写清面板数量、排版方向和边框要求。
- 让视觉节拍足够具体。

示例：

```text
Create a vertical comic-style reel with 4 equal-sized panels.
Panel 1: The owner leaves through the front door while the pet watches from the window.
Panel 2: The door clicks shut and the pet turns toward the empty house.
Panel 3: The pet sprawls across the sofa like it owns the place.
Panel 4: The owner returns and the pet sits innocently by the window.
Each panel should be clearly separated with black borders.
```

### 6. 世界知识场景

适合：特定年代、地点或历史语境下的画面。

建议：

- 直接写地点和时间。
- 再补充你关心的真实感关键词。

示例：

```text
Create a realistic outdoor crowd scene in Bethel, New York on August 16, 1969.
Photorealistic, period-accurate clothing, staging, and environment.
```

### 7. 图片文字翻译

适合：替换图片中的文字，但尽量不改版式。

示例：

```text
Translate the text in the image to Japanese. Do not change any other aspect of the image.
```

## 什么时候切换到模板

如果你遇到以下情况，优先考虑模板：

- 需要稳定复用同一种视觉结构。
- 需要把输入拆成多个具名字段。
- 需要固定的海报、写真或九宫格版式。

例如：

- 单人人像摄影：`template/portrait-photography/run.py`
- 双人写真：`template/couple-portrait/run.py`
- 街头摄影：`template/street-photography/run.py`
- 九宫格：`template/person-photoshoot-3x3/run.py`

## 输出与 history

- 通用生成图片默认输出到 `output_dir/normal/`。
- 通用生成 history 保存到仓库根目录 `history/`。

详见根目录 `README.md` 的“输出与 history”章节。
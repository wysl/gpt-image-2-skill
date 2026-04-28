# 基础图片类型规范

## 1. 信息图 (Infographic)

**用途**：解释结构化信息、教学图解、流程图、时间线

**规范**：
- 密集布局或大量文字时，使用 `quality: "high"`
- 描述信息流动和结构关系

**模板**：
```
Create a detailed Infographic of [主题].
From [组件A], to [组件B], to [组件C], etc.
Include [关键流程/关系].
清晰标注各部分，结构化布局，专业设计风格。
```

**示例**：
```
Create a detailed Infographic of the functioning and flow of an automatic coffee machine.
From bean basket, to grinding, to scale, water tank, boiler, etc.
清晰标注每个组件，展示技术流程。
```

---

## 2. 照片级写实 (Photorealism)

**用途**：人物肖像、产品摄影、场景写实

**规范**：
- 使用摄影语言（镜头、光线、构图）
- 明确要求真实纹理（毛孔、皱纹、磨损）
- 避免 studio polish、staging 等词
- 细节重要时使用 `quality: "high"`

**模板**：
```
Create a photorealistic candid photograph of [主体].
[人物细节：皮肤纹理、皱纹、毛孔等].
[动作/姿态描述].
Shot like a 35mm film photograph, [视角], using a [镜头规格].
[光线描述：soft daylight, shallow depth of field, film grain].
The image should feel honest and unposed, with real texture. No glamorization, no heavy retouching.
```

**示例**：
```
Create a photorealistic candid photograph of an elderly sailor on a fishing boat.
Weathered skin with visible wrinkles, pores, sun texture. Faded sailor tattoos.
Shot like 35mm film, medium close-up, 50mm lens.
Soft coastal daylight, shallow depth of field, subtle film grain.
Honest and unposed, real skin texture, worn materials. No heavy retouching.
```

---

## 3. Logo 设计

**用途**：品牌标志设计

**规范**：
- 描述品牌性格和用途
- 要求简洁、强形状、平衡负空间
- 可用 `n: 4` 生成多个版本
- 使用 `non-infringing` 避免版权问题

**模板**：
```
Create an original, non-infringing logo for a company called [品牌名], [行业/定位].
The logo should feel [品牌性格：warm, modern, timeless].
Use clean, vector-like shapes, strong silhouette, balanced negative space.
Favor simplicity over detail so it reads clearly at small and large sizes.
Flat design, minimal strokes, no gradients unless essential.
Plain background. Deliver a single centered logo with generous padding. No watermark.
```

**示例**：
```
Create an original, non-infringing logo for Field & Flour, a local bakery.
The logo should feel warm, simple, timeless.
Clean vector shapes, strong silhouette, balanced negative space.
Favor simplicity, reads clearly at all sizes. Flat design, no gradients.
Plain background, centered with padding. No watermark.
```

---

## 4. 广告设计 (Ad Generation)

**用途**：品牌广告、营销素材

**规范**：
- 写成创意简报形式（brand brief），而非纯技术规格
- 描述品牌、受众、文化、概念、构图、文案
- 文案用引号精确引用，要求清晰排版
- 让模型做审美决策

**模板**：
```
Give me a [风格] ad / [类型] shot for a brand called [品牌名].
[品牌定位描述].
The ad shows [场景描述] with the tagline "[文案]".
Make it feel like a polished [目标受众描述]: [风格关键词].
Use clean composition, strong color direction, natural poses.
Render the tagline exactly once, clearly and legibly, integrated into the layout.
No extra text, no watermarks, no unrelated logos.
```

**示例**：
```
Give me a cool in-culture ad for Thread, a hip street brand.
Shows friends hanging out with tagline "Yours to Create."
Polished campaign image for youth streetwear audience: stylish, contemporary, energetic.
Clean composition, strong color direction, natural poses.
Render tagline clearly and legibly. No extra text, no watermarks.
```

---

## 5. 漫画/多格图 (Story-to-Comic)

**用途**：故事转漫画、多格连环画

**规范**：
- 定义清晰的视觉节拍（visual beats），一格一个
- 描述具体、动作导向
- 指定竖版或横版排列
- 每格清晰边框分隔

**模板（4格竖版）**：
```
Create a short vertical comic-style reel with 4 equal-sized panels.
Panel 1: [场景描述、动作、对话].
Panel 2: [场景描述].
Panel 3: [场景描述].
Panel 4: [场景描述].
Each panel clearly separated with black borders, [风格关键词].
```

**模板（8格竖版）**：
```
Create a vertical comic-style layout with 8 equal-sized panels.
Panel 1: [场景描述].
Panel 2: [场景描述].
...
Panel 8: [场景描述].
Each panel clearly separated, expressive characters, [风格] style.
```

**示例**：
```
Create a short vertical comic-style reel with 4 equal-sized panels.
Panel 1: The owner leaves through the front door. Pet framed in window, eyes wide.
Panel 2: Door clicks shut. Silence. Pet turns toward empty house, posture shifting.
Panel 3: House transformed. Pet sprawls across couch like it owns the place.
Panel 4: Door opens. Pet perches innocently by window.
Each panel clearly separated, expressive characters, manga style.
```

---

## 6. 世界知识推理 (World Knowledge)

**用途**：特定历史/地点场景

**规范**：
- 描述地点、时间
- 模型会自动推断历史背景
- 使用 `photorealistic, period-accurate`

**示例**：
```
Create a realistic outdoor crowd scene in Bethel, New York on August 16, 1969.
Photorealistic, period-accurate clothing, staging, environment.
（模型会自动推断 Woodstock 音乐节背景）
```

---

## 7. 文字翻译/本地化 (Text Translation)

**用途**：翻译图片中的文字，保持设计不变

**规范**：
- 只描述翻译任务
- 强调保持其他一切不变

**模板**：
```
Translate the text in the image to [语言]. Do not change any other aspect of the image.
```
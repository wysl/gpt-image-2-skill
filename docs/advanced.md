# 高级功能规范

## 8. 虚拟试穿 (Virtual Clothing Try-on)

**用途**：将服装应用到人物照片上

**规范**：
- 需要两张参考图：人物图 + 服装图
- 描述服装如何应用到人物身上
- 保持人物身份和姿势
- 使用 `quality: "high"` 获得最佳效果

**模板**：
```
Image 1: [人物照片描述]
Image 2: [服装照片描述]

Apply the clothing from Image 2 to the person in Image 1.
Keep the person's identity, pose, and background unchanged.
The clothing should fit naturally with realistic draping and lighting.
```

**示例**：
```
Image 1: A woman standing in a casual pose, wearing a plain white t-shirt.
Image 2: A red floral summer dress on a hanger.

Apply the red floral dress from Image 2 to the woman in Image 1.
Maintain her natural pose and expression. The dress should drape realistically.
Keep the background and lighting consistent.
```

**命令**：
```bash
python3 generate.py --mode composite \
  --image person.png,clothing.png \
  --prompt "Apply the clothing from Image 2 to the person in Image 1..." \
  --quality high
```

---

## 9. 多图合成 (Multi-Image Compositing)

**用途**：将多张图片元素合成一张

**规范**：
- 用索引引用每张输入图（Image 1, Image 2...）
- 明确描述元素如何交互
- 指定哪些元素移动到哪些位置

**模板**：
```
Image 1: [描述]
Image 2: [描述]

[合成指令]: Apply [元素A] from Image 1 to [元素B] in Image 2.
Keep [保留元素] unchanged.
```

**示例**：
```
Image 1: A small bird perched on a branch.
Image 2: An elephant walking through a savanna.

Put the bird from Image 1 on the elephant's back in Image 2.
Keep the elephant's pose and the savanna background unchanged.
The bird should appear naturally scaled and lit.
```

**命令**：
```bash
python3 generate.py --mode composite \
  --image bird.png,elephant.png \
  --prompt "Put the bird from Image 1 on the elephant's back in Image 2..."
```

---

## 10. 图像编辑 (Image Editing)

**用途**：修改现有图片的特定部分

**规范**：
- 使用 "change only X" + "keep everything else the same"
- 在每次迭代中重复保留列表以减少漂移
- 对于精确编辑，说明不要改变饱和度、对比度、布局等

**模板**：
```
[基础图片描述]

Change only [要修改的部分].
Keep everything else the same: [保留元素列表].
Do not alter [饱和度、对比度、布局等].
```

**示例**：
```
A product photo of a white ceramic mug on a wooden table.

Change only the mug color to deep blue.
Keep everything else the same: the table, lighting, shadows, and camera angle.
Do not alter saturation, contrast, or the overall composition.
```

**命令**：
```bash
python3 generate.py --mode edit \
  --image mug.png \
  --prompt "Change only the mug color to deep blue. Keep everything else the same..."
```

---

## 11. 风格迁移 (Style Transfer)

**用途**：将一张图片的风格应用到另一张

**模板**：
```
Image 1: [内容图片]
Image 2: [风格参考图片]

Apply the style of Image 2 to Image 1.
Keep the content and composition of Image 1, but adopt the artistic style, color palette, and texture of Image 2.
```

**示例**：
```
Image 1: A portrait photo of a woman.
Image 2: A Van Gogh painting.

Apply the Van Gogh style from Image 2 to the portrait in Image 1.
Keep the woman's face and pose, but use impressionist brushstrokes and color palette.
```

**命令**：
```bash
python3 generate.py --mode composite \
  --image portrait.png,style.png \
  --prompt "Apply the style of Image 2 to Image 1..."
```

---

## 12. 局部重绘 (Inpainting)

**用途**：使用蒙版编辑图片的特定区域

**规范**：
- 提供蒙版图片（透明区域为可编辑区域）
- 蒙版与原图尺寸相同
- 描述要填充的内容
- 使用 `quality: "high"` 获得最佳效果

**模板**：
```
[基础图片描述]

In the masked area, generate [新内容描述].
Blend naturally with the surrounding image.
```

**示例**：
```
A landscape photo with a blank sky area.

In the masked sky area, generate a dramatic sunset with orange and purple clouds.
Blend naturally with the mountains below.
```

**命令**：
```bash
python3 generate.py --mode inpaint \
  --image landscape.png \
  --mask sky_mask.png \
  --prompt "In the masked area, generate a dramatic sunset..." \
  --quality high
```

---

## 多图输入索引规则

当提供多张参考图片时，使用以下索引方式：

| 索引 | 用法 |
|------|------|
| Image 1 | 第一张图片（`--image` 参数的第一个） |
| Image 2 | 第二张图片 |
| Image 3 | 第三张图片（最多 5 张） |

**Prompt 示例**：
```
Image 1: [描述第一张图]
Image 2: [描述第二张图]
Image 3: [描述第三张图]

[指令]: Combine elements from all images...
```

---

## 编辑约束关键词

| 关键词 | 用途 |
|--------|------|
| `change only X` | 只修改指定部分 |
| `keep everything else the same` | 保持其他所有不变 |
| `preserve identity` | 保持人物身份 |
| `preserve pose` | 保持姿态 |
| `preserve background` | 保持背景 |
| `preserve lighting` | 保持光线 |
| `do not alter saturation` | 不改变饱和度 |
| `do not alter contrast` | 不改变对比度 |
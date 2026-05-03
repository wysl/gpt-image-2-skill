# 进阶用法

本文档说明 `generate.py` 的编辑相关模式，以及多图输入时的组织方法。

## 虚拟试穿

适合：把服装参考图应用到人物参考图上。

建议：

- `Image 1` 放人物。
- `Image 2` 放服装。
- 明确要求保持身份、姿势和背景稳定。

示例：

```bash
python3 generate.py --mode composite \
  --image person.png,clothing.png \
  --prompt "Apply the clothing from Image 2 to the person in Image 1. Keep the person's identity, pose, and background unchanged." \
  --quality high
```

## 多图合成

适合：把多个来源的元素合到同一张图里。

建议：

- 在 prompt 中用 `Image 1`、`Image 2` 这样的编号引用输入图。
- 说明哪些元素要迁移，哪些部分保持不变。
- 如果是替换局部元素，写清位置和比例关系。

示例：

```bash
python3 generate.py --mode composite \
  --image bird.png,elephant.png \
  --prompt "Put the bird from Image 1 on the elephant's back in Image 2. Keep the elephant's pose and the savanna background unchanged." \
  --quality high
```

## 图片编辑

适合：在一张现有图片上做受控修改。

建议：

- 使用 `change only ...` 一类约束句式。
- 重复写出需要保留的关键元素，减少漂移。
- 如果要保持构图、饱和度、对比度，也直接写出来。

示例：

```bash
python3 generate.py --mode edit \
  --image mug.png \
  --prompt "Change only the mug color to deep blue. Keep everything else the same: the table, lighting, shadows, and camera angle. Do not alter saturation, contrast, or composition." \
  --quality high
```

## 风格迁移

适合：保留内容图的主体，把参考图的艺术风格迁过去。

示例：

```bash
python3 generate.py --mode composite \
  --image portrait.png,style.png \
  --prompt "Apply the style of Image 2 to Image 1. Keep the content and composition of Image 1, but adopt the artistic style, color palette, and texture of Image 2." \
  --quality high
```

## 局部重绘

适合：只修改蒙版区域。

要求：

- `--mask` 图片与原图尺寸一致。
- 蒙版可编辑区域应与目标区域对齐。
- prompt 只描述蒙版内要生成的内容。

示例：

```bash
python3 generate.py --mode inpaint \
  --image landscape.png \
  --mask sky-mask.png \
  --prompt "In the masked sky area, generate a dramatic sunset with orange and purple clouds. Blend naturally with the mountains below." \
  --quality high
```

## 多图输入编号规则

当使用多张参考图时，按输入顺序编号：

| 编号 | 含义 |
| --- | --- |
| `Image 1` | `--image` 参数中的第一张图 |
| `Image 2` | 第二张图 |
| `Image 3` | 第三张图 |
| `Image 4` | 第四张图 |
| `Image 5` | 第五张图 |

示例：

```text
Image 1: a portrait photo of a woman
Image 2: a watercolor painting with blue and gold tones
Image 3: a jewelry reference image

Apply the style of Image 2 to Image 1, then add the necklace from Image 3.
Keep the face, pose, and framing of Image 1 unchanged.
```

## 常用约束表达

| 表达 | 用途 |
| --- | --- |
| `change only X` | 只修改指定部分 |
| `keep everything else the same` | 保持其余内容不变 |
| `preserve identity` | 保持人物身份 |
| `preserve pose` | 保持姿态 |
| `preserve background` | 保持背景 |
| `preserve lighting` | 保持光线 |
| `do not alter saturation` | 不改变饱和度 |
| `do not alter contrast` | 不改变对比度 |

## 何时不用进阶模式

如果目标只是一次性生成新图，没有参考图或局部控制需求，直接使用：

- `generate.py --prompt ...`
- 或模板 `run.py`

通常会更稳定、也更容易复现。
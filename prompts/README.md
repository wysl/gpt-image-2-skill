# Prompt 素材库

`prompts/` 目录收录的是可复用的风格化 prompt 素材，适合人物写真、情绪化摄影和模板变量映射。

这些文件不是代码依赖项，而是给使用者和上层工作流提供的参考资料。

## 文件列表

| 文件 | 内容 |
| --- | --- |
| `学院纯欲风.md` | 学院、清纯、古风、居家等风格元素与英文模板 |
| `福利姬-中文模板.md` | 更偏性感与情绪化表达的中文模板 |

## 推荐使用方式

1. 先根据目标风格选择一个文件。
2. 从里面挑选服装、姿势、场景、光线、配饰等元素。
3. 再决定采用哪一种输出方式：
   - 直接拼成英文 prompt，用 `generate.py --prompt`。
   - 映射到 `portrait-photography` 等模板的 `--vars`。
   - 作为上层工作流中的风格素材来源。

## 何时直接走通用 prompt

适合直接写 `--prompt` 的场景：

- 你已经选好了完整元素组合。
- 你不需要模板固定版式。
- 你只是要快速试风格。

示例：

```bash
python3 generate.py \
  --prompt "portrait photography, natural window light, warm afternoon tones, young woman in a white lace dress, soft expression, bedroom background, film grain" \
  --size 1024x1536 \
  --output portrait-test.png
```

## 何时映射到模板

适合映射到模板变量的场景：

- 你希望长期复用同一视觉结构。
- 你需要把人物、妆发、服装、背景分别控制。
- 你需要稳定的九宫格、海报或封面风格。

示例：

```bash
python3 template/portrait-photography/run.py --vars '{
  "model_name": "日系少女",
  "model_appearance": "成年东亚女性，白皙肌肤，精致五官",
  "model_clothing": "白色蕾丝连衣裙",
  "model_hair": "黑色微卷长发，空气刘海",
  "background_type": "卧室白色床铺，自然窗光",
  "lighting_type": "窗边侧光，柔和暖色调",
  "pose_angle": "侧躺单手撑头",
  "mood_type": "温柔自然，高级人像摄影感"
}' --output portrait-template.png
```

## 使用时的注意事项

- 这些素材文件可能包含大量可替换元素，使用时应挑选核心视觉信息，不必整段照搬。
- 如果要对外发布工作流或示例，请不要把私有 endpoint、key 或本机路径写进 prompt 文档或示例脚本。
- 最终生成规则仍以仓库根目录 `README.md` 和模板 README 中的当前代码行为为准。
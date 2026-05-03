# couple-portrait

## 用途
用于生成双人 / 情侣写真，突出两位主体的外貌、服装、互动方式与整体氛围。

## 目录内容
- `template.json`：模板结构与占位变量
- `builder.py`：将模板变量组装为最终 prompt
- `run.py`：固定模板入口

## 关键变量
- 关系与整体：`person_a`、`person_b`、`relationship_type`
- A 角色：`person_a_name`、`person_a_appearance`、`person_a_clothing`、`person_a_pose`
- B 角色：`person_b_name`、`person_b_appearance`、`person_b_clothing`、`person_b_pose`
- 互动与场景：`interaction_type`、`background_scene`、`atmosphere`、`lighting_style`、`mood`

## 推荐调用
```bash
python3 template/couple-portrait/run.py \
  --vars '{
    "person_a": "woman",
    "person_a_name": "Ava",
    "person_a_appearance": "shoulder-length black hair and a gentle expression",
    "person_b": "man",
    "person_b_name": "Leo",
    "person_b_appearance": "short hair and a warm smile",
    "interaction_type": "leaning close and making eye contact",
    "background_scene": "a quiet cafe at sunset"
  }' \
  --output couple-portrait.png
```

## 尺寸规则
- 显式传入 `--size` 时，总是以 `--size` 为准。
- 未传 `--size` 时，本模板读取 `config.json` 中当前优先级最高 endpoint 的 `post_max_size`。
- `template.json` 里的 `aspect_ratio` / `longest side` 只表达模板意图，不是运行时硬编码默认尺寸。

## 输出与 history
- 生成历史保存在 `template/couple-portrait/history/`。
- 如果传入 `--output`，图片写到指定位置。
- 如果不传 `--output`，图片输出到 `config.json` 的 `output_dir/couple-portrait/`；未配置时使用项目默认输出目录。

## 注意事项
- `run.py` 会自动固定 `--template couple-portrait`，不要重复传 `--template`。
- README 示例请使用真实变量名；本模板没有 `subject_name`，双人信息应分别通过 `person_a_*` 与 `person_b_*` 传入。

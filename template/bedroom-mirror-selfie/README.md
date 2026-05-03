# bedroom-mirror-selfie

## 用途
用于生成卧室镜自拍风格的人像图，强调真实皮肤质感、自然居家氛围与亲密感。

## 目录内容
- `template.json`：模板结构与占位变量
- `builder.py`：将模板变量组装为最终 prompt
- `run.py`：固定模板入口

## 关键变量
- 人物：`name`、`age`、`body_type`、`expression`、`face_features`
- 姿态与造型：`pose_description`、`hair_description`、`clothing_description`
- 场景与拍摄：`bedroom_description`、`lighting_type`、`focal_length`、`mood_type`

## 推荐调用
```bash
python3 template/bedroom-mirror-selfie/run.py \
  --vars '{
    "name": "Ava",
    "age": "22",
    "expression": "soft smile",
    "pose_description": "sitting on the bed and holding the phone toward the mirror",
    "bedroom_description": "a cozy bedroom with soft window light and a slightly messy bed"
  }' \
  --output bedroom-selfie.png
```

## 尺寸规则
- 显式传入 `--size` 时，总是以 `--size` 为准。
- 未传 `--size` 时，本模板读取 `config.json` 中当前优先级最高 endpoint 的 `post_max_size`。
- `template.json` 里的 `aspect_ratio` / `longest side` 只表达模板意图，不是运行时硬编码默认尺寸。

## 输出与 history
- 生成历史保存在 `template/bedroom-mirror-selfie/history/`。
- 如果传入 `--output`，图片写到指定位置。
- 如果不传 `--output`，图片输出到 `config.json` 的 `output_dir/bedroom-mirror-selfie/`；未配置时使用项目默认输出目录。

## 注意事项
- `run.py` 会自动固定 `--template bedroom-mirror-selfie`，不要重复传 `--template`。
- README 示例请使用真实变量名；本模板没有 `subject_name`，应使用 `name`、`age`、`pose_description` 等字段。

# couple-portrait

## 作用
- 模板定义：`template.json`
- Prompt 组装：`builder.py`
- 固定入口：`run.py`

## 目录规则
- 模板 history 存放位置：`template/couple-portrait/history/`
- 图片 output 存放位置：`~/.hermes/output/gpt-image-2/couple-portrait/`
- output 目录可在 `config.json` 的 `output_dir` 字段中自定义

## 默认信息
- 模板显示名：couple-portrait
- 默认质量：high
- 默认比例：9:16
- 默认最长边：3840
- 默认尺寸：2160x3840

## 支持的默认变量
- `atmosphere`
- `background_scene`
- `interaction_type`
- `lighting_style`
- `mood`
- `person_a`
- `person_a_appearance`
- `person_a_clothing`
- `person_a_name`
- `person_a_pose`
- `person_b`
- `person_b_appearance`
- `person_b_clothing`
- `person_b_name`
- `person_b_pose`
- `relationship_type`

## 推荐调用
```bash
cd template/couple-portrait
python3 run.py --vars '{"subject_name":"Ava & Leo"}' --output couple.png --timeout 500
```

## 注意事项
- 此模板没有单独的动态场景生成逻辑
- 模板行为主要由 `template.json` + `builder.py` 决定



## 默认尺寸规则

本模板在未显式传 `--size` 时，读取 `config.json` 中当前优先级最高 endpoint 的 `post_max_size`。

如果显式传了 `--size`，则始终以用户传入尺寸为准。

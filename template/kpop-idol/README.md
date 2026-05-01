# kpop-idol

## 作用
- 模板定义：`template.json`
- Prompt 组装：`builder.py`
- 固定入口：`run.py`

## 目录规则
- 模板 history 存放位置：`template/kpop-idol/history/`
- 图片 output 存放位置：`~/.hermes/output/gpt-image-2/kpop-idol/`
- output 目录可在 `config.json` 的 `output_dir` 字段中自定义

## 默认信息
- 模板显示名：kpop-idol
- 默认质量：high
- 默认比例：9:16
- 默认最长边：3840
- 默认尺寸：2160x3840

## 支持的默认变量
- `background_type`
- `color_theme`
- `idol_appearance`
- `idol_concept`
- `idol_costume`
- `idol_group`
- `idol_makeup_hair`
- `idol_name`
- `lighting_effect`
- `mood_type`
- `pose_type`

## 推荐调用
```bash
cd template/kpop-idol
python3 run.py --vars '{"subject_name":"Minji"}' --output kpop.png --timeout 500
```

## 注意事项
- 此模板没有单独的动态场景生成逻辑
- 模板行为主要由 `template.json` + `builder.py` 决定

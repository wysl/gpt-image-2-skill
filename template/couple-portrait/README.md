# couple-portrait

## 作用
- 模板定义：`template.json`
- Prompt 组装：`builder.py`
- 固定入口：`run.py`

## 目录规则
- 模板 history 存放位置：`/root/.openclaw/skills/gpt-image-2/template/couple-portrait/history/`
- 图片 output 存放位置：`/root/.openclaw/skills/gpt-image-2/output/`
- 也就是说：**history 按模板分流，output 仍然统一落在 skill 根目录**

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
cd /root/.openclaw/skills/gpt-image-2/template/couple-portrait
python3 run.py --vars '{"subject_name":"Ava & Leo"}' --output couple.png --timeout 500
```

## 注意事项
- 此模板没有单独的动态场景生成逻辑
- 模板行为主要由 `template.json` + `builder.py` 决定

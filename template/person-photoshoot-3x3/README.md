# person-photoshoot-3x3

## 作用
- 模板定义：`template.json`
- Prompt 组装：`builder.py`
- 固定入口：`run.py`
- 动态场景生成：`scene_generator.py`

## 目录规则
- 模板 history 存放位置：`/root/.openclaw/skills/gpt-image-2/template/person-photoshoot-3x3/history/`
- 图片 output 存放位置：`/root/.openclaw/skills/gpt-image-2/output/`
- 也就是说：**history 按模板分流，output 仍然统一落在 skill 根目录**

## 默认信息
- 模板显示名：人物写真3x3
- 默认质量：high
- 默认比例：9:16
- 默认最长边：3840
- 默认尺寸：2160x3840

## 支持的默认变量
- `aesthetic_style`
- `background_scene`
- `bottom_center_pose`
- `bottom_left_pose`
- `bottom_right_pose`
- `expression_style`
- `hair_style`
- `lighting_style`
- `makeup_style`
- `mid_center_pose`
- `mid_left_pose`
- `mid_right_pose`
- `mood_style`
- `outfit_style`
- `poster_style`
- `required_keyword`
- `series_style`
- `skin_texture`
- `subject_name`
- `subject_type`
- `subtitle_text`
- `tagline_text`
- `title_text`
- `tone_style`
- `top_center_pose`
- `top_left_pose`
- `top_right_pose`

## 推荐调用
```bash
cd /root/.openclaw/skills/gpt-image-2/template/person-photoshoot-3x3
python3 run.py --vars '{"subject_name":"Minji","required_keyword":"100% 一致性"}' --output person-3x3.png --timeout 500
```

## 注意事项
- 该模板包含 `scene_generator.py`
- 若未显式传入 `panel_1 ~ panel_9`，会自动调用 LLM 生成动态场景
- 若你传入了 `panel_1 ~ panel_9`，则优先使用你提供的场景

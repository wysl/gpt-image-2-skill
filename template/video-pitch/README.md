# video-pitch

## 作用
- 模板定义：`template.json`
- Prompt 组装：`builder.py`
- 固定入口：`run.py`
- 附加脚本：`generate_pitchdeck.py`
- 附加脚本：`combine_panels.py`

## 目录规则
- 模板 history 存放位置：`/root/.openclaw/skills/gpt-image-2/template/video-pitch/history/`
- 图片 output 存放位置：`/root/.openclaw/skills/gpt-image-2/output/`
- 也就是说：**history 按模板分流，output 仍然统一落在 skill 根目录**

## 默认信息
- 模板显示名：video-pitch
- 默认质量：high
- 默认比例：9:16
- 默认最长边：未设置
- 默认尺寸：1440x2560

## 支持的默认变量
- `ambient_sound`
- `camera_style`
- `color1_hex`
- `color1_name`
- `color1_use`
- `color2_hex`
- `color2_name`
- `color2_use`
- `color3_hex`
- `color3_name`
- `color3_use`
- `color4_hex`
- `color4_name`
- `color4_use`
- `color_mood`
- `core_conflict`
- `core_scene`
- `duration`
- `emotional_arc`
- `emotional_peak`
- `ending_style`
- `female_age`
- `female_appearance`
- `female_char`
- `female_costume`
- `female_keywords`
- `female_role`
- `female_turnaround`
- `film_refs`
- `genre`
- `key_dialogue`
- `key_props`
- `key_shot_types`
- `key_sound_effects`
- `light_feature1`
- `light_feature2`
- `light_feature3`
- `lighting_style`
- `male_age`
- `male_appearance`
- `male_char`
- `male_costume`
- `male_keywords`
- `male_role`
- `male_turnaround`
- `music_genre`
- `one_line_synopsis`
- `opening_style`
- `overall_pacing`
- `period_setting`
- `ref1`
- `ref2`
- `ref3`
- `ref4`
- `scene_mood`
- `season`
- `story_flow`
- `subtitle`
- `target_audience`
- `time_of_day`
- `title`
- `transition_style`
- `video_type`
- `visual_style`
- `weather`
- `weather_effect`

## 推荐调用
```bash
cd /root/.openclaw/skills/gpt-image-2/template/video-pitch
python3 run.py --vars '{"title":"PROJECT TITLE"}' --output pitch.png --timeout 500
```

## 视频模板附加调用
```bash
python3 generate_pitchdeck.py --vars '{"title":"PROJECT TITLE"}'
python3 combine_panels.py --images img1.png,img2.png,img3.png --layout vertical
```

## 注意事项
- 此模板没有单独的动态场景生成逻辑
- 模板行为主要由 `template.json` + `builder.py` 决定

# video-pitch

## 用途
- `video-pitch` 的固定模板入口，调用 `run.py` 时会自动路由到根目录 `generate.py`，并强制使用 `--template video-pitch`
- 模板内容定义在 `template.json`
- Prompt 组装逻辑在 `builder.py`
- 额外提供 `generate_pitchdeck.py` 用于 3-panel pitch deck 生成，`combine_panels.py` 用于拼接 panel 图片

## 目录内容
- `template.json`：模板内容、默认变量与 3-panel 约束
- `builder.py`：将模板转换为最终 prompt
- `run.py`：固定模板入口脚本
- `generate_pitchdeck.py`：按 panel 规则拆分生成多张图
- `combine_panels.py`：拼接已生成的 panel 图片
- `history/`：该模板的请求历史目录

## 关键变量
- 标题与项目信息：`title`、`subtitle`、`video_type`、`duration`、`genre`、`target_audience`
- 故事：`one_line_synopsis`、`core_conflict`、`emotional_arc`、`story_flow`、`key_dialogue`
- 角色：`female_char`、`female_age`、`female_role`、`female_appearance`、`female_keywords`、`female_costume`、`female_turnaround`、`male_char`、`male_age`、`male_role`、`male_appearance`、`male_keywords`、`male_costume`、`male_turnaround`
- 场景与镜头：`core_scene`、`scene_mood`、`time_of_day`、`season`、`weather`、`weather_effect`、`camera_style`、`key_shot_types`、`transition_style`
- 节奏与声音：`overall_pacing`、`emotional_peak`、`opening_style`、`ending_style`、`music_genre`、`ambient_sound`、`key_sound_effects`
- 色彩与灯光：`color_mood`、`color1_name`~`color4_use`、`lighting_style`、`light_feature1`、`light_feature2`、`light_feature3`
- 参考：`film_refs`、`ref1`、`ref2`、`ref3`、`ref4`

## 推荐调用
```bash
cd template/video-pitch
python3 run.py --vars '{"title":"PROJECT TITLE"}' --output pitch.png --timeout 500

python3 generate_pitchdeck.py --vars '{"title":"PROJECT TITLE"}'
python3 combine_panels.py --images img1.png,img2.png,img3.png --layout vertical
```

## 尺寸规则
- 显式传入 `--size` 时，始终以 `--size` 为准
- 未传 `--size` 时，本模板使用当前最高优先级已启用 endpoint 的 `design_max_size`

## 输出与 history
- history 写入：`template/video-pitch/history/`
- 图片输出目录：`config.json` 的 `output_dir` + `/video-pitch`
- 未配置 `output_dir` 时，默认输出到：`~/.hermes/output/gpt-image-2/video-pitch/`
- `run.py` 的相对 `--output`、`generate_pitchdeck.py` 生成的 panel 图片，以及 `combine_panels.py` 的输出都会落到该模板输出目录

## 注意事项
- `run.py` 会自动固定模板名，不要再额外传 `--template`
- `generate_pitchdeck.py` 会按脚本内定义拆成 3 个 panel，且将人物信息限制在 panel 1
- `combine_panels.py` 读取图片时，传相对文件名会优先从模板输出目录中查找
- `builder.py` 使用通用模板转 prompt 逻辑；若变量未展开，会在运行时输出占位符警告

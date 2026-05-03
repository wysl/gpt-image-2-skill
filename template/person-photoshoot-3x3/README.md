# person-photoshoot-3x3

## 用途
- 模板定义：`template.json`
- Prompt 组装：`builder.py`
- 固定入口：`run.py`
- 动态场景生成：`scene_generator.py`
- 用于生成 9:16 的人物写真 3x3 九宫格海报，并强调同一人物在九张图中的一致性

## 目录内容
- `template.json`：模板结构、默认变量、质量与比例配置
- `builder.py`：在有 endpoint provider 时先补全动态场景，再拼接最终 prompt
- `scene_generator.py`：在未提供用户场景时，通过 chat completions 生成 `panel_1` 到 `panel_9`
- `run.py`：固定使用 `person-photoshoot-3x3` 模板的运行入口
- `history/`：模板调用历史，运行后写入 `template/person-photoshoot-3x3/history/`

## 关键变量
- `required_keyword`
- `subject_name`
- `subject_type`
- `series_style`
- `poster_style`
- `aesthetic_style`
- `tone_style`
- `makeup_style`
- `skin_texture`
- `expression_style`
- `hair_style`
- `outfit_style`
- `background_scene`
- `lighting_style`
- `mood_style`
- `title_text`
- `subtitle_text`
- `tagline_text`
- `top_left_pose`
- `top_center_pose`
- `top_right_pose`
- `mid_left_pose`
- `mid_center_pose`
- `mid_right_pose`
- `bottom_left_pose`
- `bottom_center_pose`
- `bottom_right_pose`
- `panel_1` ~ `panel_9`（如显式提供，则优先使用）

## 推荐调用
```bash
cd template/person-photoshoot-3x3
python3 run.py --vars '{"subject_name":"Minji","required_keyword":"100% 一致性"}' --output person-3x3.png --timeout 500
```

## 尺寸规则
- 这些模板默认走 `post_max_size`，显式 `--size` 优先。
- 模板自身仍保留 `quality` 与 `aspect_ratio` 配置，供 prompt/build 阶段和未显式覆盖时使用。

## 输出与 history
- 默认 output 目录：`~/.hermes/output/gpt-image-2/person-photoshoot-3x3/`
- 若 `config.json` 配置了 `output_dir`，则输出会写入该目录下的模板子目录
- history 目录：`template/person-photoshoot-3x3/history/`

## 注意事项
- `run.py` 会固定注入 `--template person-photoshoot-3x3`，不要重复传 `--template`
- `builder.py` 在存在 `endpoint_provider` 时会先调用 `scene_generator.py`
- 若未显式传入用户场景，`scene_generator.py` 会尝试生成 `panel_1` 到 `panel_9`
- 若已提供用户场景，则优先使用你传入的 `panel_1` 到 `panel_9`
- 模板关键词和调用变量中应保留 `required_keyword`，默认值为 `100% 一致性`

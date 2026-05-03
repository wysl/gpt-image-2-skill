# street-photography

## 用途
- 模板定义：`template.json`
- Prompt 组装：`builder.py`
- 固定入口：`run.py`
- 用于生成街头摄影风格图像，场景、人物、镜头和后期语义都由模板变量控制

## 目录内容
- `template.json`：模板结构、默认变量、质量与比例配置
- `builder.py`：将模板字段和 `--vars` 变量拼接为最终 prompt
- `run.py`：固定使用 `street-photography` 模板的运行入口
- `history/`：模板调用历史，运行后写入 `template/street-photography/history/`

## 关键变量
- `street_location`
- `city_name`
- `district_type`
- `style_type`
- `main_subject`
- `subject_type`
- `subject_pose`
- `focal_length`
- `aperture`
- `angle_of_view`
- `depth_of_field`
- `lighting_condition`
- `light_direction`
- `light_quality`
- `light_color_temp`
- `composition_style`
- `camera_angle`
- `frame_element`
- `leading_lines`
- `color_palette`
- `contrast_level`
- `saturation_level`
- `processing_style`
- `grain_level`
- `bw_toggle`
- `mood`
- `story_element`
- `moment_type`
- `time_of_day`
- `weather`
- `interaction_type`

## 推荐调用
```bash
cd template/street-photography
python3 run.py --vars '{"street_location":"Shibuya crossing at night","main_subject":"a stylish young woman under neon lights"}' --output street.png --timeout 500
```

## 尺寸规则
- 这些模板默认走 `post_max_size`，显式 `--size` 优先。
- 模板自身仍保留 `quality` 与 `aspect_ratio` 配置，供 prompt/build 阶段和未显式覆盖时使用。

## 输出与 history
- 默认 output 目录：`~/.hermes/output/gpt-image-2/street-photography/`
- 若 `config.json` 配置了 `output_dir`，则输出会写入该目录下的模板子目录
- history 目录：`template/street-photography/history/`

## 注意事项
- `run.py` 会固定注入 `--template street-photography`，不要重复传 `--template`
- `builder.py` 会对未替换的占位符打印 warning
- 此模板没有单独的动态场景生成逻辑

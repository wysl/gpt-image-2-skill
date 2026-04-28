# street-photography

## 作用
- 模板定义：`template.json`
- Prompt 组装：`builder.py`
- 固定入口：`run.py`

## 目录规则
- 模板 history 存放位置：`/root/.openclaw/skills/gpt-image-2/template/street-photography/history/`
- 图片 output 存放位置：`/root/.openclaw/skills/gpt-image-2/output/`
- 也就是说：**history 按模板分流，output 仍然统一落在 skill 根目录**

## 默认信息
- 模板显示名：street-photography
- 默认质量：high
- 默认比例：9:16
- 默认最长边：3840
- 默认尺寸：2160x3840

## 支持的默认变量
- `angle_of_view`
- `aperture`
- `atmosphere_type`
- `bw_toggle`
- `camera_angle`
- `city_name`
- `color_palette`
- `composition_style`
- `contrast_level`
- `depth_of_field`
- `district_type`
- `focal_length`
- `frame_element`
- `grain_level`
- `interaction_type`
- `leading_lines`
- `light_color_temp`
- `light_direction`
- `light_quality`
- `lighting_condition`
- `main_subject`
- `moment_type`
- `mood`
- `processing_style`
- `saturation_level`
- `story_element`
- `street_location`
- `style_type`
- `subject_pose`
- `subject_type`
- `time_of_day`
- `weather`

## 推荐调用
```bash
cd /root/.openclaw/skills/gpt-image-2/template/street-photography
python3 run.py --vars '{"subject_name":"City girl"}' --output street.png --timeout 500
```

## 注意事项
- 此模板没有单独的动态场景生成逻辑
- 模板行为主要由 `template.json` + `builder.py` 决定

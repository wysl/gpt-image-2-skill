# anime-girl-and-man-date-photo-collage-3x3

## 作用
- 模板定义：`template.json`
- Prompt 组装：`builder.py`
- 固定入口：`run.py`
- 动态场景生成：`scene_generator.py`

## 目录规则
- 模板 history 存放位置：`template/anime-girl-and-man-date-photo-collage-3x3/history/`
- 图片 output 存放位置：`~/.hermes/output/gpt-image-2/anime-girl-and-man-date-photo-collage-3x3/`
- output 目录可在 `config.json` 的 `output_dir` 字段中自定义

## 默认信息
- 模板显示名：二次元少女与男生约会拼贴3x3
- 默认质量：high
- 默认比例：9:16
- 默认最长边：3840
- 默认尺寸：2160x3840

## 支持的默认变量
- `anime_girl_subject`
- `background_scene`
- `lighting_style`
- `man_subject`
- `mood_style`
- `panel_1`
- `panel_2`
- `panel_3`
- `panel_4`
- `panel_5`
- `panel_6`
- `panel_7`
- `panel_8`
- `panel_9`
- `poster_style`
- `required_keyword`
- `subtitle_text`
- `tagline_text`
- `title_text`

## 推荐调用
```bash
cd template/anime-girl-and-man-date-photo-collage-3x3
python3 run.py --vars '{"title_text":"Date Collage","required_keyword":"100% 一致性"}' --output anime-date-3x3.png --timeout 500
```

## 注意事项
- 该模板包含 `scene_generator.py`
- 若未显式传入 `panel_1 ~ panel_9`，会自动调用 LLM 生成动态场景
- 若你传入了 `panel_1 ~ panel_9`，则优先使用你提供的场景

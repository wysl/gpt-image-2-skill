# anime-girl-and-man-date-photo-collage-3x3

## 用途
用于生成 9:16 的 3x3 约会拼贴海报：男主保持真人摄影质感，女主保持二次元 / 2D 动漫质感，并在 9 个分镜中维持一致性。

## 目录内容
- `template.json`：模板结构与占位变量
- `builder.py`：将模板变量组装为最终 prompt
- `run.py`：固定模板入口
- `scene_generator.py`：可选的 9 宫格动态场景生成

## 关键变量
- 主体：`man_subject`、`anime_girl_subject`、`required_keyword`
- 风格与文案：`poster_style`、`background_scene`、`lighting_style`、`mood_style`、`title_text`、`subtitle_text`、`tagline_text`
- 九宫格分镜：`panel_1` 到 `panel_9`

## 推荐调用
```bash
python3 template/anime-girl-and-man-date-photo-collage-3x3/run.py \
  --vars '{
    "man_subject": "a real adult man with short dark hair and a plain dark shirt",
    "anime_girl_subject": "an anime-style young woman with blonde twin ponytails and large blue eyes",
    "required_keyword": "100% 一致性",
    "title_text": "Date Collage"
  }' \
  --output anime-date-3x3.png
```

## 尺寸规则
- 显式传入 `--size` 时，总是以 `--size` 为准。
- 未传 `--size` 时，本模板读取 `config.json` 中当前优先级最高 endpoint 的 `post_max_size`。
- `template.json` 里的 `aspect_ratio` / `longest side` 只表达模板意图，不是运行时硬编码默认尺寸。

## 输出与 history
- 生成历史保存在 `template/anime-girl-and-man-date-photo-collage-3x3/history/`。
- 如果传入 `--output`，图片写到指定位置。
- 如果不传 `--output`，图片输出到 `config.json` 的 `output_dir/anime-girl-and-man-date-photo-collage-3x3/`；未配置时使用项目默认输出目录。

## 注意事项
- `run.py` 会自动固定 `--template anime-girl-and-man-date-photo-collage-3x3`，不要重复传 `--template`。
- 若未提供 `panel_1` 到 `panel_9`，`scene_generator.py` 会尝试通过支持 chat completions 的 endpoint 生成分镜。
- 若需要完全可控的九宫格内容，请显式传入 `panel_1` 到 `panel_9`。
- 动态场景辅助逻辑额外接受 `theme`，并兼容 `girl_subject` 作为 `anime_girl_subject` 的别名；但模板本身的正式变量仍是 `anime_girl_subject`。

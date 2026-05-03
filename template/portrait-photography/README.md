# portrait-photography

## 用途
- `portrait-photography` 的固定模板入口，调用 `run.py` 时会自动路由到根目录 `generate.py`，并强制使用 `--template portrait-photography`
- 模板内容定义在 `template.json`
- Prompt 组装逻辑在 `builder.py`

## 目录内容
- `template.json`：模板内容与默认变量
- `builder.py`：将模板转换为最终 prompt
- `run.py`：固定模板入口脚本
- `history/`：该模板的请求历史目录

## 关键变量
- 人物主体：`model_name`、`model_appearance`、`model_clothing`、`model_makeup`、`model_hair`
- 画面控制：`pose_angle`、`background_type`、`lighting_type`、`mood_type`

## 推荐调用
```bash
cd template/portrait-photography
python3 run.py --vars '{"model_name":"Ava"}' --output portrait.png --timeout 500
```

## 尺寸规则
- 显式传入 `--size` 时，始终以 `--size` 为准
- 未传 `--size` 时，本模板使用当前最高优先级已启用 endpoint 的 `post_max_size`

## 输出与 history
- history 写入：`template/portrait-photography/history/`
- 图片输出目录：`config.json` 的 `output_dir` + `/portrait-photography`
- 未配置 `output_dir` 时，默认输出到：`~/.hermes/output/gpt-image-2/portrait-photography/`
- `--output` 传相对路径时，文件会写入模板输出目录；传绝对路径时，按绝对路径保存

## 注意事项
- `run.py` 会自动固定模板名，不要再额外传 `--template`
- 模板默认不添加文字内容，`typography` 仅提供简洁排版框架
- `builder.py` 会根据 `aspect_ratio` 和 `longest side` 生成模板内的基础尺寸，但实际生成优先遵循 CLI 的尺寸规则

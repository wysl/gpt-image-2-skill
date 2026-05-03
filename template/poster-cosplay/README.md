# poster-cosplay

## 用途
- `poster-cosplay` 的固定模板入口，调用 `run.py` 时会自动路由到根目录 `generate.py`，并强制使用 `--template poster-cosplay`
- 模板内容定义在 `template.json`
- Prompt 组装逻辑在 `builder.py`

## 目录内容
- `template.json`：模板内容与默认变量
- `builder.py`：将模板转换为最终 prompt
- `run.py`：固定模板入口脚本
- `history/`：该模板的请求历史目录

## 关键变量
- `xxx`：角色名或角色描述，会替换模板中的 `[xxx]`

## 推荐调用
```bash
cd template/poster-cosplay
python3 run.py --vars '{"xxx":"莎赫拉查德 Code S from Brown Dust 2"}' --output poster.png --timeout 500
```

## 尺寸规则
- 显式传入 `--size` 时，始终以 `--size` 为准
- 未传 `--size` 时，本模板使用当前最高优先级已启用 endpoint 的 `post_max_size`

## 输出与 history
- history 写入：`template/poster-cosplay/history/`
- 图片输出目录：`config.json` 的 `output_dir` + `/poster-cosplay`
- 未配置 `output_dir` 时，默认输出到：`~/.hermes/output/gpt-image-2/poster-cosplay/`
- `--output` 传相对路径时，文件会写入模板输出目录；传绝对路径时，按绝对路径保存

## 注意事项
- `run.py` 会自动固定模板名，不要再额外传 `--template`
- 模板排版规则来自 `template.json` 的 `typography`，其中非主题文字使用中文
- 本模板的 prompt 结构由 `builder.py` 定义，包含人物、服装、环境、构图、灯光、氛围与文字层级

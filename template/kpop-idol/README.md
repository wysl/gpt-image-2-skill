# kpop-idol

## 用途
- 模板定义：`template.json`
- Prompt 组装：`builder.py`
- 固定入口：`run.py`
- 用于生成韩流偶像风格写真，主体与氛围变量由 `template.json` 的占位符驱动

## 目录内容
- `template.json`：模板结构、默认变量、质量与比例配置
- `builder.py`：将模板字段和 `--vars` 变量拼接为最终 prompt
- `run.py`：固定使用 `kpop-idol` 模板的运行入口
- `history/`：模板调用历史，运行后写入 `template/kpop-idol/history/`

## 关键变量
- `idol_name`
- `idol_group`
- `idol_appearance`
- `idol_makeup_hair`
- `idol_costume`
- `idol_concept`
- `pose_type`
- `background_type`
- `lighting_effect`
- `color_theme`
- `mood_type`

## 推荐调用
```bash
cd template/kpop-idol
python3 run.py --vars '{"idol_name":"Minji"}' --output kpop.png --timeout 500
```

## 尺寸规则
- 这些模板默认走 `post_max_size`，显式 `--size` 优先。
- 模板自身仍保留 `quality` 与 `aspect_ratio` 配置，供 prompt/build 阶段和未显式覆盖时使用。

## 输出与 history
- 默认 output 目录：`~/.hermes/output/gpt-image-2/kpop-idol/`
- 若 `config.json` 配置了 `output_dir`，则输出会写入该目录下的模板子目录
- history 目录：`template/kpop-idol/history/`

## 注意事项
- `run.py` 会固定注入 `--template kpop-idol`，不要重复传 `--template`
- `builder.py` 会对未替换的占位符打印 warning
- 此模板没有单独的动态场景生成逻辑

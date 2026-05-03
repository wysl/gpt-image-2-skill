# SKILL.md

本文件面向把这个仓库作为 Claude Skill、自动化脚本或其他上层工作流接入的读者，重点说明稳定入口、目录约定和调用规则。

## 适用范围

这个仓库提供两类能力：

- 通用入口：`generate.py`
- 模板入口：`template/<template-name>/run.py`

其中：

- `generate.py` 负责 API 调用、模板解析、history 保存、尺寸决策和输出分流。
- 每个模板目录自带独立的 `template.json`、`builder.py`、`run.py`，便于单独维护。

## 公开入口

### 通用入口

```text
generate.py
```

用途：

- 文生图
- 编辑已有图片
- 多图合成
- 局部重绘
- 加载模板并传入 `--vars`

### 模板入口

```text
template/poster-cosplay/run.py
template/video-pitch/run.py
template/video-pitch/generate_pitchdeck.py
template/video-pitch/combine_panels.py
template/portrait-photography/run.py
template/couple-portrait/run.py
template/kpop-idol/run.py
template/street-photography/run.py
template/bedroom-mirror-selfie/run.py
template/person-photoshoot-3x3/run.py
template/anime-girl-and-man-date-photo-collage-3x3/run.py
```

调用模板时，优先使用目录内的 `run.py`，不要额外传 `--template`。

## 模板目录结构

每个模板都使用相同结构：

```text
template/<template-name>/
├── README.md
├── template.json
├── builder.py
├── run.py
└── history/
```

特殊情况：

- `template/video-pitch/` 还包含 `generate_pitchdeck.py` 和 `combine_panels.py`。
- `template/person-photoshoot-3x3/` 和 `template/anime-girl-and-man-date-photo-collage-3x3/` 还包含 `scene_generator.py`，在未显式提供完整 panel 内容时会动态补场景。

## 历史与输出规则

### history

- 通用生成：`history/`
- 模板生成：`template/<template-name>/history/`

### output

output 根目录由 `config.json.output_dir` 决定；未配置时默认：

```text
~/.hermes/output/gpt-image-2
```

在该目录下自动分流：

- 通用生成：`normal/`
- 模板生成：`<template-name>/`

这一规则适用于：

- `generate.py`
- 所有模板 `run.py`
- `template/video-pitch/generate_pitchdeck.py`
- `template/video-pitch/combine_panels.py`

## 配置方式

配置文件为仓库根目录下的 `config.json`，公开示例为 `config.json.example`。

支持：

- 多 endpoint 按优先级回退
- 每个 endpoint 独立 timeout
- endpoint 级默认尺寸配置
- 自定义 output 根目录

相关关键字段：

| 字段 | 含义 |
| --- | --- |
| `priority` | endpoint 优先级，越小越先尝试 |
| `enabled` | 是否启用该 endpoint |
| `timeout` | 单次请求超时 |
| `post_max_size` | 非 `video-pitch` 模板默认尺寸 |
| `design_max_size` | 通用生成和 `video-pitch` 默认尺寸 |
| `output_dir` | 输出根目录 |

## 尺寸规则

实际运行逻辑如下：

- 显式传 `--size` 时，始终以该值为准。
- 未传 `--size` 时：
  - `generate.py` 使用当前最高优先级 endpoint 的 `design_max_size`。
  - `video-pitch` 使用当前最高优先级 endpoint 的 `design_max_size`。
  - 其他模板使用当前最高优先级 endpoint 的 `post_max_size`。

不要把模板 README 中的静态尺寸数字当作强约束；真实默认值由当前 endpoint 配置决定。

## 通用 CLI 参数

`generate.py` 的核心参数：

| 参数 | 说明 |
| --- | --- |
| `--prompt` | 通用 prompt |
| `--template` | 模板名 |
| `--vars` | 模板变量 JSON |
| `--list-templates` | 列出模板 |
| `--mode` | `generate` / `edit` / `composite` / `inpaint` |
| `--size` | 输出尺寸 |
| `--quality` | 当前仅支持 `high` |
| `--n` | 生成数量 |
| `--output` | 输出文件名 |
| `--timeout` | 本次请求超时 |
| `--image` | 参考图路径，多个用逗号分隔 |
| `--mask` | inpaint 蒙版图 |

模板 `run.py` 是轻量包装器，主要做两件事：

1. 固定 `--template`。
2. 把 history/output 路由到对应模板目录。

## `video-pitch` 特殊入口

### `generate_pitchdeck.py`

```bash
python3 template/video-pitch/generate_pitchdeck.py \
  --vars '{"title":"PROJECT TITLE"}' \
  --prefix pitch \
  [--size 1440x2560] \
  [--timeout 500] \
  [--no-combine]
```

行为：

- 生成 `panel-1`、`panel-2`、`panel-3` 三张图。
- 默认会继续调用 `combine_panels.py` 生成一张拼接图。
- 未传 `--size` 时，默认读取当前最高优先级 endpoint 的 `design_max_size`。

### `combine_panels.py`

```bash
python3 template/video-pitch/combine_panels.py \
  --images a.png,b.png,c.png \
  --layout vertical \
  [--cols 2] \
  [--labels "Part 1,Part 2,Part 3"] \
  [--output combined.png]
```

也支持自动模式：

```bash
python3 template/video-pitch/combine_panels.py --auto --prefix pitch --max 5
```

## 模板选择建议

- 单人写真：`portrait-photography`
- 双人关系感画面：`couple-portrait`
- 偶像/概念照：`kpop-idol`
- 日常自拍：`bedroom-mirror-selfie`
- 街头纪实感：`street-photography`
- 九宫格一致性表达：`person-photoshoot-3x3`
- 二次元女性 + 真人男性组合：`anime-girl-and-man-date-photo-collage-3x3`
- 带封面排版的角色海报：`poster-cosplay`
- 项目方案三联页：`video-pitch`

## 发布与仓库卫生

对外发布时，不要提交以下本地文件：

- `config.json`
- `history/`
- `template/*/history/`
- 任何包含真实 key、私有 endpoint 或本机专用路径的文件

如果需要给用户示例配置，只保留 `config.json.example`。
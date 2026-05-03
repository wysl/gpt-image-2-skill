# poster-cosplay

## 作用
- 模板定义：`template.json`
- Prompt 组装：`builder.py`
- 固定入口：`run.py`

## 目录规则
- 模板 history 存放位置：`template/poster-cosplay/history/`
- 图片 output 存放位置：`~/.hermes/output/gpt-image-2/poster-cosplay/`
- output 目录可在 `config.json` 的 `output_dir` 字段中自定义

## 默认信息
- 模板显示名：Cosplay角色海报
- 默认质量：high
- 默认比例：9:16
- 默认最长边：3840
- 默认尺寸：2160x3840

## 支持的默认变量
- `xxx` - 角色名/描述（用于替换占位符）

## 排版规则
- **非主题文字使用中文**
- 文字层级：
  1. 主标题 - [xxx]（高对比纤细衬线体或中文宋体）
  2. 副标题 - [xxx]名称或皮肤名（中等字重中文黑体）
  3. 中文短标语（细中文宋体）
  4. 期号 + 发布信息（中文细黑体）
  5. 条形码 + ISBN（标准条码字体）

## 推荐调用
```bash
cd template/poster-cosplay
python3 run.py --vars '{"xxx":"莎赫拉查德 Code S from Brown Dust 2"}' --output poster.png --timeout 500
```

## 注意事项
- 此模板没有单独的动态场景生成逻辑
- 模板行为主要由 `template.json` + `builder.py` 决定
- 排版层级已整理为清晰的5级结构
- 非主题文字统一使用中文


## 默认尺寸规则

本模板在未显式传 `--size` 时，读取 `config.json` 中当前优先级最高 endpoint 的 `post_max_size`。

如果显式传了 `--size`，则始终以用户传入尺寸为准。

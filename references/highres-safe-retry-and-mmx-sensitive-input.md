# GPT-Image-2 本轮会话补充：高分辨率保守重试与发送验证

## 1. 2160x3840 人像被 sexual safety 拦截时的处理

触发场景：
- 单人古风/写真图
- 姿势描述包含明显挑逗、触唇、吐舌、纯欲、透视露肤等词
- 4K 竖版请求（2160x3840）

观察到的错误：
- `HTTP 500 ... safety_violations=[sexual]`
- 其他 fallback 端点可能同时出现 `系统繁忙，请稍后再试`

有效策略：
- **不降分辨率**（用户明确要求时）
- 把 prompt 改写成：
  - 成年化主体
  - 杂志/时尚摄影语言
  - 构图描述保留，诱导性解释删除
  - 服装改成古风层叠/刺绣/轻纱，不强调露肤

成功输出：
- 文件：`/root/.hermes/output/gpt-image-2/portrait-photography/hanfu-portrait-2160-safe.png`
- 尺寸：`2160x3840`

## 2. Telegram 大图发送超时不等于生成失败

现象：
- `send_message` 发送 `MEDIA:/...png` 时超时
- 但生成脚本已经成功返回 `Saved: ...png`

结论：
- 先把“生成成功”和“发送成功”分开判断
- 若发送失败，优先验证本地文件存在与尺寸，而不是误判为生图失败

## 3. PNG 尺寸验证：不要依赖 Pillow

本轮环境里：
- `ModuleNotFoundError: No module named 'PIL'`

可靠方式：
- 用 Python 标准库 `struct` 读取 PNG IHDR 头
- 前 24 字节中：
  - `16:20` = width
  - `20:24` = height

示例结果：
- `2160x3840`

## 4. MiniMax Vision 对敏感图片会在输入阶段直接拦截

对图像 `/root/.hermes/image_cache/img_2a6e4ad39804.jpg`，即便 prompt 改成纯姿态分析、只提几何构图，也返回：

- `API error: input new_sensitive, input image sensitive (HTTP 200)`

说明：
- 不是提示词措辞问题，而是 **输入图像级别** 的敏感拦截
- 这类情况下不能声称“mmx 分析得出……”，只能如实说明未获得模型正文输出
- 可退而求其次：基于用户提供的图像描述，整理一版人工改写的姿态分析稿，并明确不是 mmx 实际返回

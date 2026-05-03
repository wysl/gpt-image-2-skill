# Endpoint behavior notes — 2026-05-03

聚焦 `poster-cosplay` 与通用接口在不同端点/尺寸下的真实行为。

## 已验证结果

### 1. `88996.cloud`

- 直连 `2160x3840`：HTTP 200，可返回图片
- 但在 `poster-cosplay` 模板与通用直调的多次测试中，**实际文件静默降级为 `941x1672`**
- 该现象在更短、更保守 prompt 下仍复现，说明**不是 prompt 长度问题**，更像端点/链路侧行为

### 2. `bltcy.ai`

- 通用接口 + `1024x1536`：稳定成功
- `poster-cosplay` 模板 + `1024x1536`：稳定成功
- `poster-cosplay` 模板 + `1440x2560`：稳定成功，且**按请求尺寸原样返回**
- `1080x2048`：可出图，但此尺寸不是 16 的倍数，且实测返回 `911x1726`，不推荐
- 直连 `2160x3840`：出现 `RemoteDisconnected('Remote end closed connection without response')`

### 3. `xflow`

- 直连 `2160x3840`：出现 `RemoteDisconnected('Remote end closed connection without response')`

## 当前可操作结论

### 对 `poster-cosplay` 模板：

**默认优先：**
- `bltcy.ai + 1024x1536`
- `bltcy.ai + 1440x2560`

**不推荐：**
- `1080x2048`（非法尺寸，不是 16 的倍数）
- 把 `2160x3840` 当作 `poster-cosplay` 的稳定真 4K 输出

### 对 4K 请求：

- 即使日志显示 `Size: 2160x3840`，也必须实际读取 PNG 头校验真实尺寸
- 汇报时同时写：
  - 请求尺寸
  - 实际返回尺寸
  - 命中端点

## 推荐表述模板

- `请求尺寸：2160x3840；实际返回尺寸：941x1672；端点：88996.cloud；状态：HTTP 200 但静默降级。`
- `请求尺寸：1440x2560；实际返回尺寸：1440x2560；端点：bltcy.ai；状态：成功且尺寸准确。`

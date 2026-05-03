# GPT-Image-2 Skill

使用 GPT-Image-2 API 生成高质量图片，支持文生图、图生图、局部编辑、多图合成、模板生成等能力。

## 模板生成效果展示

<table>
<tr>
<td align="center"><img src="example/poster-cosplay-example.png" width="300" height="400"><br><b>Cosplay角色海报</b></td>
<td align="center"><img src="example/video-pitch-example.png" width="300" height="400"><br><b>Pitch Deck 3联拼贴</b></td>
<td align="center"><img src="example/portrait-photography-example.png" width="300" height="400"><br><b>人像摄影</b></td>
</tr>
<tr>
<td align="center"><img src="example/couple-portrait-example.png" width="300" height="400"><br><b>情侣双人写真</b></td>
<td align="center"><img src="example/kpop-idol-example.png" width="300" height="400"><br><b>K-pop偶像写真</b></td>
<td align="center"><img src="example/street-photography-example.png" width="300" height="400"><br><b>街头摄影</b></td>
</tr>
<tr>
<td align="center"><img src="example/bedroom-mirror-selfie-example.png" width="300" height="400"><br><b>卧室镜自拍</b></td>
<td align="center"><img src="example/person-photoshoot-3x3-example.png" width="300" height="400"><br><b>人物写真九宫格</b></td>
<td align="center"><img src="example/anime-date-collage-3x3-example.png" width="300" height="400"><br><b>动漫少女与真人约会拼贴</b></td>
</tr>
</table>

---

## 目录结构

```
gpt-image-2-skill/
├── config.json           # API 配置（需要填写您的 url 和 key）
├── generate.py           # 通用入口脚本
├── README.md             # 本文档
├── SKILL.md              # Skill 说明文档
├── example/              # 示例图片
├── docs/                 # 详细文档
│   ├── basic.md          # 基础用法
│   └── advanced.md       # 高级用法
├── prompts/              # 风格化提示词素材库（生成人物写真时必读）
│   ├── README.md         # 索引与使用流程
│   ├── 学院纯欲风.md     # 学院纯欲/清纯/古风/居家 风格元素 + 15个英文生图模板
│   └── 福利姬-中文模板.md # 福利姬/性感诱惑 风格元素 + 6个中文模板
└── template/             # 模板目录
    ├── poster-cosplay/
    │   ├── template.json
    │   ├── builder.py
    │   ├── run.py
    │   └── README.md
    ├── video-pitch/
    │   ├── template.json
    │   ├── builder.py
    │   ├── run.py
    │   ├── generate_pitchdeck.py
    │   ├── combine_panels.py
    │   └ README.md
    ├── portrait-photography/
    ├── couple-portrait/
    ├── kpop-idol/
    ├── street-photography/
    ├── bedroom-mirror-selfie/
    ├── person-photoshoot-3x3/
    │   ├── template.json
    │   ├── builder.py
    │   ├── run.py
    │   ├── scene_generator.py
    │   └ README.md
    └── anime-girl-and-man-date-photo-collage-3x3/
        ├── template.json
        ├── builder.py
        ├── run.py
        ├── scene_generator.py
        └ README.md
```

## 快速开始

### 1. 配置 API

编辑 `config.json`，填写您的 API url 和 key：

```json
{
  "endpoints": [
    {
      "name": "your-provider",
      "url": "xxxxx",
      "model": "gpt-image-2",
      "key": "xxxxx",
      "priority": 1,
      "timeout": 500,
      "enabled": true
    }
  ],
  "default_model": "gpt-image-2",
  "retry_count": 1
}
```

### 2. 基础用法

#### 文生图（通用 prompt）

```bash
python3 generate.py --prompt "一位优雅的少女站在樱花树下，日系风格" --size 1024x1536 --quality high
```

#### 使用模板

```bash
# poster-cosplay 模板
python3 template/poster-cosplay/run.py --vars '{"xxx":"狐女"}'

# portrait-photography 模板
python3 template/portrait-photography/run.py --vars '{"model_name":"美少女"}'

# video-pitch 模板（生成3张pitch deck）
python3 template/video-pitch/generate_pitchdeck.py --vars '{"title":"项目名称","subtitle":"副标题"}'
```

## 风格化提示词库

`prompts/` 目录存放按风格分类的**可直接用于生图的提示词素材库**，涵盖服装、姿势、配饰、光线、场景、妆容、后期调色等完整元素。

| 文件 | 风格 | 适用场景 | 大小 |
|------|------|----------|------|
| `prompts/学院纯欲风.md` | 学院纯欲/清纯/古风/居家 | 校园清新、软萌甜美、汉服古风、慵懒居家 | ~27KB |
| `prompts/福利姬-中文模板.md` | 福利姬/性感诱惑 | 制服诱惑、清纯无辜、大胆写真、慵懒居家 | ~22KB |

**使用流程：**
1. 确定风格 → 读取对应 `prompts/xxx.md`
2. 从服装+姿势+配饰+场景+光线中各选一项组合
3. 使用文件中的英文模板直接作为 `--prompt`，或映射到 `portrait-photography` 模板 vars
4. 按安全规则降敏后生成

详见 `prompts/README.md`。

**快速示例：**

```bash
# 从学院纯欲风模板12（JK制服+教室）直接生图
cd ~/.hermes/skills/gpt-image-2
python3 generate.py --prompt "portrait photography, natural window light streaming through classroom windows, warm afternoon golden hour tones, young woman wearing white shirt with plaid skirt, hair in low ponytail with ribbon, sitting on desk edge, legs dangling, holding book close to chest, shy smile, nostalgic school atmosphere, film grain" --size 1024x1536 --output jk-classroom.png --timeout 500

# 从元素库混搭，映射到 portrait-photography 模板
cd template/portrait-photography
python3 run.py --vars '{
  "model_appearance":"成年东亚女性，白皙肌肤，精致五官，神情温柔",
  "model_clothing":"白色蕾丝连衣裙，缎面质感，珍珠纽扣装饰",
  "model_hair":"黑色微卷长发，空气刘海，珍珠发夹",
  "model_makeup":"水光唇釉，大地色眼影，腮红晕染",
  "background_type":"卧室白色床铺，自然窗光",
  "lighting_type":"窗边侧光，柔和暖色调",
  "pose_angle":"侧躺单手撑头，双腿微曲，慵懒自然",
  "mood_type":"温柔纯欲，清新自然，高级人像摄影感"
}' --output pure-desire-bedroom.png --timeout 500
```


## 端点尺寸配置

`config.json` 中每个 endpoint 支持两个尺寸字段：

- `post_max_size`：模板生成默认尺寸（除 `video-pitch` 外的所有模板）
- `design_max_size`：通用生成与 `video-pitch` 默认尺寸

当前约定：
- `88996.cloud`：`post_max_size=2160x3840`，`design_max_size=1440x2560`
- `bltcy.ai`：`post_max_size=1440x2560`，`design_max_size=1440x2560`
- `xflow`：`post_max_size=1440x2560`，`design_max_size=1440x2560`

脚本规则：
- 显式传 `--size` 时，以用户参数为准
- 未传 `--size` 时：
  - `video-pitch` 用当前优先级最高 endpoint 的 `design_max_size`
  - 其他所有模板用当前优先级最高 endpoint 的 `post_max_size`
  - 通用 `generate.py` 用当前优先级最高 endpoint 的 `design_max_size`

## 模板列表

| 模板 | 说明 | 特点 |
|------|------|------|
| `poster-cosplay` | Cosplay角色海报 | 电影级海报风格，杂志封面质感 |
| `video-pitch` | 视频方案Pitch Deck | 3张图拆分：角色设计+色彩方案+声音设计 |
| `portrait-photography` | 人像摄影 | 高端杂志封面风格 |
| `couple-portrait` | 情侣双人写真 | 亲密感、甜蜜氛围 |
| `kpop-idol` | K-pop偶像写真 | 韩流偶像风格，舞台级妆发 |
| `street-photography` | 街头摄影 | 纪实感，城市氛围 |
| `bedroom-mirror-selfie` | 卧室镜自拍 | 私密自拍风格，真实肌肤质感 |
| `person-photoshoot-3x3` | 人物写真3x3 | 九宫格拼贴，100%一致性 |
| `anime-girl-and-man-date-photo-collage-3x3` | 动漫少女与真人约会拼贴 | 二次元少女+真人男生，3x3拼贴 |

## 模板使用示例

### poster-cosplay

```bash
python3 template/poster-cosplay/run.py \
  --vars '{"xxx":"莎赫拉查德 Code S from Brown Dust 2"}' \
  --output poster.png \
  --timeout 500
```

**输出**：
- 图片：`~/.hermes/output/gpt-image-2/poster-cosplay/poster.png`
- History：`template/poster-cosplay/history/YYYYMMDD-HHMMSS.json`

---

### video-pitch

```bash
python3 template/video-pitch/generate_pitchdeck.py \
  --vars '{"title":"剑舞乱世","subtitle":"乱世江湖·剑影传奇","genre":"武侠动作"}' \
  --prefix my_pitch \
  --timeout 500
```

**输出**：
- `~/.hermes/output/gpt-image-2/video-pitch/my_pitch-panel-1.png`（角色设计+故事板）
- `~/.hermes/output/gpt-image-2/video-pitch/my_pitch-panel-2.png`（项目信息+道具插画）
- `~/.hermes/output/gpt-image-2/video-pitch/my_pitch-panel-3.png`（色彩+灯光+声音）
- `~/.hermes/output/gpt-image-2/video-pitch/my_pitch-full-pitchdeck.png`（拼接版）

---

### portrait-photography

```bash
python3 template/portrait-photography/run.py \
  --vars '{"model_name":"日系少女","model_appearance":"20岁东亚少女"}' \
  --output portrait.png \
  --timeout 500
```

---

### couple-portrait

```bash
python3 template/couple-portrait/run.py \
  --vars '{"person_a_name":"女生","person_b_name":"男生"}' \
  --output couple.png \
  --timeout 500
```

---

### kpop-idol

```bash
python3 template/kpop-idol/run.py \
  --vars '{"idol_name":"Jennie风格","idol_group":"BLACKPINK"}' \
  --output kpop.png \
  --timeout 500
```

---

### street-photography

```bash
python3 template/street-photography/run.py \
  --vars '{"main_subject":"东亚少女","street_location":"东京涩谷"}' \
  --output street.png \
  --timeout 500
```

---

### bedroom-mirror-selfie

```bash
python3 template/bedroom-mirror-selfie/run.py \
  --vars '{"name":"甜美少女","clothing_description":"粉色宽松睡裙"}' \
  --output selfie.png \
  --timeout 500
```

---

### person-photoshoot-3x3

```bash
python3 template/person-photoshoot-3x3/run.py \
  --vars '{"subject_name":"日系少女","subject_type":"young East Asian female idol"}' \
  --output photoshoot_3x3.png \
  --timeout 500
```

**特点**：九宫格拼贴，保持100%人物一致性

---

### anime-girl-and-man-date-photo-collage-3x3

```bash
python3 template/anime-girl-and-man-date-photo-collage-3x3/run.py \
  --vars '{"anime_girl_subject":"动漫少女","man_subject":"东亚真人男生"}' \
  --output anime_date.png \
  --timeout 500
```

**特点**：二次元动漫少女 + 真人男生约会场景，3x3九宫格拼贴

---

## History 与 Output 规则

### History 存储位置

- **模板调用**：`template/<模板名>/history/`
- **通用 prompt**：`history/`（根目录）

### Output 存储位置

- **通用 prompt 生成的图片**：`~/.hermes/output/gpt-image-2/normal/`
- **模板生成的图片**：`~/.hermes/output/gpt-image-2/<template-name>/`
- output 目录可在 `config.json` 的 `output_dir` 字段中自定义

### 示例

```
# 模板调用
template/poster-cosplay/history/20260428-123456.json
~/.hermes/output/gpt-image-2/poster-cosplay/poster.png

# 通用 prompt
history/20260428-123456.json
~/.hermes/output/gpt-image-2/normal/20260428-123456.png
```

## 高级功能

### 图片编辑（edit）

```bash
python3 generate.py --mode edit \
  --image photo.png \
  --prompt "改为专业模特拍摄姿势"
```

### 多图合成（composite）

```bash
python3 generate.py --mode composite \
  --image img1.png,img2.png,img3.png \
  --prompt "将三张图片合成一张杂志封面"
```

### 局部重绘（inpaint）

```bash
python3 generate.py --mode inpaint \
  --image photo.png \
  --mask mask.png \
  --prompt "将衣服改为红色"
```

## API 配置说明

### endpoints 字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | Endpoint 名称 | `"88996.cloud"` |
| `url` | API 地址 | `"https://xxxxx"` |
| `model` | 模型名称 | `"gpt-image-2"` |
| `key` | API Key | `"xxxxx"` |
| `priority` | 优先级（数字越小优先级越高） | `1` |
| `timeout` | 超时时间（秒） | `500` |
| `enabled` | 是否启用 | `true` |

### 多 endpoint 配置

支持配置多个 API endpoint，按 priority 顺序尝试：

```json
{
  "endpoints": [
    {
      "name": "primary",
      "url": "xxxxx",
      "key": "xxxxx",
      "priority": 1,
      "enabled": true
    },
    {
      "name": "backup",
      "url": "xxxxx",
      "key": "xxxxx",
      "priority": 2,
      "enabled": true
    }
  ]
}
```

## 参数说明

### generate.py 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 图片描述 | 必填 |
| `--template` | 模板名称 | 无 |
| `--vars` | 模板变量（JSON） | 无 |
| `--size` | 图片尺寸 | `1024x1536` |
| `--quality` | 图片质量 | `high` |
| `--n` | 生成数量（1-4） | `1` |
| `--output` | 输出文件名 | 自动生成 |
| `--timeout` | 超时时间（秒） | `500` |
| `--mode` | 模式（generate/edit/composite/inpaint） | `generate` |

### 模板 run.py 参数

| 参数 | 说明 |
|------|------|
| `--vars` | 模板变量（JSON 格式） |
| `--output` | 输出文件名 |
| `--timeout` | 超时时间（秒） |

## 常见问题

### 1. 图片尺寸警告

```
Warning: Max edge >= 3840px, results may be unstable
```

**解决**：这是提示性警告，不影响生成。如遇到不稳定问题，可将 `longest side` 调小。

### 2. 模板变量未扩展

```
⚠️ WARNING: Template has 2 unexpanded placeholders: ['xxx', 'yyy']
```

**解决**：使用 `--vars` 提供缺失的变量值：

```bash
python3 template/poster-cosplay/run.py --vars '{"xxx":"角色名","yyy":"其他变量"}'
```

### 3. endpoint 连接失败

```
Error: All endpoints failed
```

**解决**：
1. 检查 `config.json` 中的 `url` 和 `key` 是否正确
2. 检查网络连接
3. 尝试使用其他 endpoint（设置不同的 priority）

## 依赖

- Python 3.8+
- requests
- Pillow（用于 video-pitch 图片拼接）

## 安装依赖

```bash
pip install requests Pillow
```

## 版本历史

### v5.2.0

- 模板目录化重构
- 9个模板独立目录
- history 按模板分目录存储
- output 统一放在 ~/.hermes/output/gpt-image-2/ 下，按模板/normal 分目录
- 修复 combine_panels.py 和 generate_pitchdeck.py 路径问题
- 添加示例图片预览

## 作者

- **Author**: _wysl
- **Version**: 5.2.0

## 许可证

MIT License
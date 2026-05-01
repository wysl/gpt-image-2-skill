#!/usr/bin/env python3
"""
GPT-Image-2 图片生成工具（支持多 endpoint fallback 和模板）

用法：
    python3 generate.py --prompt "..." [--size 1024x1536] [--quality high] [--n 1]
    python3 template/poster-cosplay/run.py --vars '{"xxx":"角色名"}' [--output poster.png] [--timeout 500]
    python3 generate.py --mode edit --image photo.png --prompt "Change..."
    python3 generate.py --mode composite --image img1.png,img2.png --prompt "Combine..."
    python3 generate.py --mode inpaint --image photo.png --mask mask.png --prompt "Fill..."
"""

import argparse
import json
import base64
import os
import sys
import requests
import importlib.util
from pathlib import Path
from datetime import datetime

# 目录配置
SKILL_DIR = Path(__file__).parent.resolve()
HISTORY_DIR = SKILL_DIR / "history"
CONFIG_FILE = SKILL_DIR / "config.json"
TEMPLATE_DIR = SKILL_DIR / "template"
DEFAULT_OUTPUT_DIR = "~/.hermes/output/gpt-image-2"


def resolve_history_dir(template_name=None):
    if template_name:
        return TEMPLATE_DIR / template_name / "history"
    return HISTORY_DIR


def resolve_output_dir(template_name=None):
    """解析输出目录：从 config.json 读取 output_dir，按模板/普通模式分流。"""
    config = load_config()
    base = Path(config.get('output_dir', DEFAULT_OUTPUT_DIR)).expanduser()
    if template_name:
        return base / template_name
    return base / 'normal'

# 全局配置
CONFIG = None

def load_config():
    """加载配置文件"""
    global CONFIG
    if CONFIG is not None:
        return CONFIG
    
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            CONFIG = json.load(f)
    else:
        # 默认配置（fallback）
        CONFIG = {
            "endpoints": [
                {
                    "name": "tokenflux",
                    "url": "https://api.bltcy.ai/v1",
                    "model": "gpt-image-2",
                    "key": os.getenv("GPT_IMAGE_KEY", ""),
                    "priority": 1,
                    "timeout": 200,
                    "enabled": True
                }
            ],
            "default_model": "gpt-image-2",
            "retry_count": 3
        }
    return CONFIG

def get_endpoints():
    """获取按优先级排序的可用 endpoints"""
    config = load_config()
    endpoints = sorted(
        [ep for ep in config.get("endpoints", []) if ep.get("enabled", True)],
        key=lambda x: x.get("priority", 999)
    )
    return endpoints

def list_templates():
    """列出所有可用模板目录。"""
    if not TEMPLATE_DIR.exists():
        return []
    templates = set()
    for d in TEMPLATE_DIR.iterdir():
        if d.is_dir() and (d / "template.json").exists():
            templates.add(d.name)
    return sorted(templates)


def load_template(template_name):
    """加载模板文件，只读取 template/<name>/template.json。"""
    template_file = TEMPLATE_DIR / template_name / "template.json"
    if not template_file.exists():
        print(f"Error: Template '{template_name}' not found")
        print(f"Available templates: {list_templates()}")
        sys.exit(1)

    with open(template_file) as f:
        return json.load(f)


def load_template_builder(template_name):
    builder_path = TEMPLATE_DIR / template_name / "builder.py"
    if str(SKILL_DIR) not in sys.path:
        sys.path.insert(0, str(SKILL_DIR))
    builder_dir = str(builder_path.parent)
    if builder_dir not in sys.path:
        sys.path.insert(0, builder_dir)
    if builder_path.exists():
        module_name = f"template_builder_{template_name.replace('-', '_')}"
        spec = importlib.util.spec_from_file_location(module_name, builder_path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module
    raise SystemExit(f"Error: No template builder module for '{template_name}' (expected {builder_path})")


def template_to_prompt(template_name, template, variables=None):
    """将模板转换为 prompt；每个模板有独立 builder 模块。"""
    builder = load_template_builder(template_name)
    return builder.build_prompt(template, variables or {}, get_endpoints)


def validate_size(size):
    """验证分辨率是否符合约束"""
    try:
        w, h = map(int, size.lower().split('x'))
        
        # 检查 16 倍数
        if w % 16 != 0 or h % 16 != 0:
            print(f"Warning: Size {size} is not a multiple of 16")
        
        # 检查最大边缘
        if max(w, h) >= 3840:
            print(f"Warning: Max edge >= 3840px, results may be unstable")
        
        # 检查比例
        ratio = max(w, h) / min(w, h)
        if ratio > 3:
            print(f"Error: Aspect ratio {ratio:.1f}:1 exceeds 3:1 limit")
            sys.exit(1)
        
        # 检查总像素
        total_pixels = w * h
        if total_pixels > 8294400:
            print(f"Error: Total pixels {total_pixels} exceeds limit 8,294,400")
            sys.exit(1)
        if total_pixels < 655360:
            print(f"Error: Total pixels {total_pixels} below limit 655,360")
            sys.exit(1)
        
        return size
    except ValueError:
        print(f"Error: Invalid size format '{size}', use 'WxH' like '1024x1536'")
        sys.exit(1)


def call_api_with_fallback(path, payload=None, files=None, data=None, timeout_override=None):
    """按 endpoint 优先级顺序调用 API，直到成功。"""
    endpoints = get_endpoints()
    if not endpoints:
        raise SystemExit("Error: No enabled endpoints configured")

    retry_count = load_config().get("retry_count", 1)
    errors = []

    for ep in endpoints:
        base_url = ep["url"].rstrip("/")
        url = f"{base_url}{path}"
        model = ep.get("model") or load_config().get("default_model", "gpt-image-2")
        timeout = timeout_override or ep.get("timeout", 200)
        headers = {"Authorization": f"Bearer {ep['key']}"}

        print(f"  Trying endpoint: {ep['name']} ({base_url})")

        for attempt in range(1, retry_count + 1):
            try:
                if payload is not None:
                    request_payload = dict(payload)
                    request_payload.setdefault("model", model)
                    resp = requests.post(
                        url,
                        headers={**headers, "Content-Type": "application/json"},
                        json=request_payload,
                        timeout=timeout,
                    )
                else:
                    request_data = dict(data or {})
                    request_data.setdefault("model", model)
                    resp = requests.post(
                        url,
                        headers=headers,
                        data=request_data,
                        files=files,
                        timeout=timeout,
                    )

                if resp.ok:
                    return resp.json()

                errors.append(f"{ep['name']} attempt {attempt}: HTTP {resp.status_code} {resp.text[:300]}")
            except Exception as e:
                errors.append(f"{ep['name']} attempt {attempt}: {e}")

    print("Error: All endpoints failed")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)


def save_history(payload, response_data, timestamp, history_dir=None):
    """保存请求历史"""
    history_dir = history_dir or HISTORY_DIR
    history_dir.mkdir(parents=True, exist_ok=True)
    history_file = history_dir / f"{timestamp}.json"
    history = {
        "timestamp": timestamp,
        "request": payload,
        "response": {
            "created": response_data.get("created"),
            "image_count": len(response_data.get("data", []))
        }
    }
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    return history_file

def generate_image(prompt, size="1024x1536", quality="high", n=1, output=None, timeout_override=None, history_dir=None, template_name=None):
    """基础图片生成"""
    validate_size(size)
    
    # 确保输出目录存在
    out_dir = resolve_output_dir(template_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    history_dir = history_dir or HISTORY_DIR
    history_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # 默认输出文件名
    if output is None:
        output = out_dir / f"{timestamp}.png"
    else:
        # 如果用户指定了路径，检查是否是相对路径
        if not Path(output).is_absolute():
            output = out_dir / output
    
    # API payload - 使用 b64_json 格式
    payload = {
        "prompt": prompt,
        "n": n,
        "size": size,
        "quality": quality,
        "response_format": "b64_json"
    }
    
    print(f"Generating {n} image(s) with gpt-image-2...")
    print(f"  Size: {size}")
    print(f"  Quality: {quality}")
    
    # 调用 API（带 fallback）
    data = call_api_with_fallback("/images/generations", payload=payload, timeout_override=timeout_override)
    
    if 'data' not in data:
        print(f"Error: No image data in response: {data}")
        sys.exit(1)
    
    # 保存请求历史
    history_file = save_history(payload, data, timestamp, history_dir=history_dir)
    print(f"  History: {history_file}")
    
    # 保存图片
    for i, item in enumerate(data['data']):
        # 支持两种响应格式：url 或 b64_json
        img_url = item.get('url')
        b64 = item.get('b64_json')
        
        if img_url:
            # URL 格式：下载图片
            img_response = requests.get(img_url, timeout=60)
            img_bytes = img_response.content
        elif b64:
            # b64_json 格式：解码
            # 检查是否是 Data URL 格式（data:image/png;base64,<data>）
            if b64.startswith('data:'):
                # 去掉前缀
                # 格式：data:image/png;base64,<actual_base64>
                prefix_end = b64.find(',') + 1
                b64 = b64[prefix_end:]
            # 处理 padding
            padding_needed = 4 - (len(b64) % 4)
            if padding_needed != 4:
                b64 += '=' * padding_needed
            img_bytes = base64.b64decode(b64)
        else:
            print(f"Error: No url or b64_json in response")
            sys.exit(1)
        
        filename = str(output) if n == 1 else str(out_dir / f"{timestamp}_{i+1}.png")
        
        with open(filename, 'wb') as f:
            f.write(img_bytes)
        
        print(f"  Saved: {filename} ({len(img_bytes)} bytes)")
    
    return True

def edit_image(images, prompt, size="1024x1536", quality="high", output=None, timeout_override=None, history_dir=None, template_name=None):
    """图片编辑（使用 multipart/form-data 格式）"""
    
    # 确保输出目录存在
    out_dir = resolve_output_dir(template_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    history_dir = history_dir or HISTORY_DIR
    history_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    if output is None:
        output = out_dir / f"{timestamp}.png"
    elif not Path(output).is_absolute():
        output = out_dir / output
    
    # 准备 multipart 数据
    files_data = []
    for i, img_path in enumerate(images):
        with open(img_path, 'rb') as f:
            files_data.append(('image', (Path(img_path).name, f.read(), 'image/png')))
        print(f"  Image {i+1}: {img_path}")
    
    data = {
        'prompt': prompt,
        'n': '1',
        'size': size,
        'quality': quality
    }
    
    print(f"Editing image...")
    
    # 调用 API（带 fallback）
    result = call_api_with_fallback("/images/edits", files=files_data, data=data, timeout_override=timeout_override)
    
    if 'data' not in result:
        print(f"Error: No image data in response")
        sys.exit(1)
    
    # API 返回两张图片：第一张是原图，最后一张是编辑后的图
    # 取最后一张作为编辑结果
    item = result['data'][-1]
    
    # 支持两种响应格式：url 或 b64_json
    img_url = item.get('url')
    b64 = item.get('b64_json')
    
    if img_url:
        img_response = requests.get(img_url, timeout=60)
        img_bytes = img_response.content
    elif b64:
        # 检查是否是 Data URL 格式
        if b64.startswith('data:'):
            prefix_end = b64.find(',') + 1
            b64 = b64[prefix_end:]
        # 处理 padding
        padding_needed = 4 - (len(b64) % 4)
        if padding_needed != 4:
            b64 += '=' * padding_needed
        img_bytes = base64.b64decode(b64)
    else:
        print(f"Error: No url or b64_json in response")
        sys.exit(1)
    
    with open(str(output), 'wb') as out_f:
        out_f.write(img_bytes)
    
    # 保存历史
    history_file = save_history({'images': images, 'prompt': prompt}, result, timestamp, history_dir=history_dir)
    print(f"  History: {history_file}")
    print(f"  Saved: {output} ({len(img_bytes)} bytes)")
    return True

def inpaint_image(image_path, mask_path, prompt, size="1024x1024", quality="high", output=None, timeout_override=None, history_dir=None, template_name=None):
    """局部重绘（蒙版编辑）- 使用 multipart/form-data 格式"""
    
    # 确保输出目录存在
    out_dir = resolve_output_dir(template_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    history_dir = history_dir or HISTORY_DIR
    history_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    if output is None:
        output = out_dir / f"{timestamp}.png"
    elif not Path(output).is_absolute():
        output = out_dir / output
    
    # 准备 multipart 数据
    with open(image_path, 'rb') as img_f:
        img_data = img_f.read()
    with open(mask_path, 'rb') as mask_f:
        mask_data = mask_f.read()
    
    files_data = [
        ('image', (Path(image_path).name, img_data, 'image/png')),
        ('mask', (Path(mask_path).name, mask_data, 'image/png'))
    ]
    
    data = {
        'prompt': prompt,
        'n': '1',
        'size': size,
        'quality': quality
    }
    
    print(f"Inpainting...")
    print(f"  Image: {image_path}")
    print(f"  Mask: {mask_path}")
    
    # 调用 API（带 fallback）
    result = call_api_with_fallback("/images/edits", files=files_data, data=data)
    
    if 'data' not in result:
        print(f"Error: No image data in response")
        sys.exit(1)
    
    # API 返回两张图片：第一张是原图，最后一张是编辑后的图
    # 取最后一张作为编辑结果
    item = result['data'][-1]
    
    # 支持两种响应格式：url 或 b64_json
    img_url = item.get('url')
    b64 = item.get('b64_json')
    
    if img_url:
        img_response = requests.get(img_url, timeout=60)
        img_bytes = img_response.content
    elif b64:
        # 检查是否是 Data URL 格式
        if b64.startswith('data:'):
            prefix_end = b64.find(',') + 1
            b64 = b64[prefix_end:]
        # 处理 padding
        padding_needed = 4 - (len(b64) % 4)
        if padding_needed != 4:
            b64 += '=' * padding_needed
        img_bytes = base64.b64decode(b64)
    else:
        print(f"Error: No url or b64_json in response")
        sys.exit(1)
    
    with open(str(output), 'wb') as out_f:
        out_f.write(img_bytes)
    
    # 保存历史
    history_file = save_history({'image': image_path, 'mask': mask_path, 'prompt': prompt}, result, timestamp, history_dir=history_dir)
    print(f"  History: {history_file}")
    print(f"  Saved: {output} ({len(img_bytes)} bytes)")
    return True

def main():
    parser = argparse.ArgumentParser(
        description='GPT-Image-2 通用入口：支持通用 prompt、模板生成、edit/composite/inpaint',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # 模板参数
    parser.add_argument('--template', default=None, help='模板名称（不带 .json 扩展名）')
    parser.add_argument('--vars', default=None, help='模板变量（JSON 格式，如 {"subject":"狐女"}）')
    parser.add_argument('--list-templates', action='store_true', help='列出所有可用模板')
    
    # 模式选择
    parser.add_argument('--mode', choices=['generate', 'edit', 'composite', 'inpaint'],
                        default='generate', help='操作模式')
    
    # 基础参数
    parser.add_argument('--prompt', default=None, help='图片描述（支持中文，使用模板时可选）')
    parser.add_argument('--size', default='1024x1536', help='分辨率，如 1024x1536')
    parser.add_argument('--quality', choices=['high'], default='high',
                        help='图片质量：high（固定使用高质量）')
    parser.add_argument('--n', type=int, default=1, choices=range(1, 5),
                        help='生成数量（1-4）')
    parser.add_argument('--output', default=None, help='输出文件名（默认保存到 output_dir/模板名/ 或 output_dir/normal/ 目录）')
    parser.add_argument('--timeout', type=int, default=500, help='临时覆盖当前请求超时（秒），默认 500 秒；不修改 config.json')
    
    # 编辑模式参数
    parser.add_argument('--image', help='参考图片路径（多个用逗号分隔）')
    parser.add_argument('--mask', help='蒙版图片路径（局部重绘）')
    
    args = parser.parse_args()
    
    # 列出模板
    if args.list_templates:
        templates = list_templates()
        print("Available templates:")
        for t in templates:
            print(f"  - {t}")
        return
    
    # 模板处理
    template_prompt = None
    template_size = None
    template_quality = None
    history_dir = resolve_history_dir(args.template) if args.template else HISTORY_DIR
    
    if args.template:
        template = load_template(args.template)
        # 读取模板的默认值
        defaults = template.get("defaults", {})
        variables = defaults.copy()  # 以 defaults 为基础
        variables["_template_name"] = args.template  # 传递模板名给 scene 生成函数
        if args.vars:
            try:
                user_vars = json.loads(args.vars)
                # 检测用户是否传了 panel 场景覆盖
                has_user_panels = any(k.startswith("panel_") for k in user_vars)
                if has_user_panels:
                    user_vars["_user_provided_panels"] = True
                variables.update(user_vars)  # 用户变量覆盖默认值
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in --vars: {e}")
                sys.exit(1)
        template_prompt, template_size, template_quality = template_to_prompt(args.template, template, variables)
        print(f"Template: {args.template}")
        print(f"Generated prompt: {template_prompt[:200]}...")
    
    # 确定 prompt（模板优先，用户参数覆盖）
    prompt = args.prompt or template_prompt
    if not prompt:
        print("Error: --prompt required (or use --template)")
        sys.exit(1)
    
    # 确定参数（仅在用户显式传参时覆盖模板；否则使用模板值）
    user_provided_size = any(arg in sys.argv for arg in ['--size', '--size=', '-s'])
    user_provided_quality = any(arg in sys.argv for arg in ['--quality'])

    size = args.size if user_provided_size else (template_size or '1024x1536')
    quality = args.quality if user_provided_quality else (template_quality or 'high')
    
    # 根据模式执行
    if args.mode == 'generate':
        generate_image(
            prompt=prompt,
            size=size,
            quality=quality,
            n=args.n,
            output=args.output,
            timeout_override=args.timeout,
            history_dir=history_dir,
            template_name=args.template,
        )
    
    elif args.mode == 'edit':
        if not args.image:
            print("Error: --image required for edit mode")
            sys.exit(1)
        images = args.image.split(',')
        edit_image(
            images=images,
            prompt=prompt,
            size=size,
            quality=quality,
            output=args.output,
            timeout_override=args.timeout,
            history_dir=history_dir,
            template_name=args.template,
        )
    
    elif args.mode == 'composite':
        if not args.image:
            print("Error: --image required for composite mode")
            sys.exit(1)
        images = args.image.split(',')
        if len(images) < 2:
            print("Error: Composite mode requires at least 2 images")
            sys.exit(1)
        edit_image(
            images=images,
            prompt=prompt,
            size=size,
            quality=quality,
            output=args.output,
            timeout_override=args.timeout,
            history_dir=history_dir,
            template_name=args.template,
        )
    
    elif args.mode == 'inpaint':
        if not args.image or not args.mask:
            print("Error: --image and --mask required for inpaint mode")
            sys.exit(1)
        inpaint_image(
            image_path=args.image,
            mask_path=args.mask,
            prompt=prompt,
            size=size,
            quality=args.quality,
            output=args.output,
            timeout_override=args.timeout,
            history_dir=history_dir,
            template_name=args.template,
        )

if __name__ == '__main__':
    main()
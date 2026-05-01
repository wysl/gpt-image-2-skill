#!/usr/bin/env python3
"""
多图拼接工具 - 用于 video-pitch 模板的多张图片组合

用法：
    python3 combine_panels.py --images img1.png,img2.png,img3.png --layout vertical
    python3 combine_panels.py --images img1.png,img2.png --layout horizontal
    python3 combine_panels.py --images img1.png,img2.png,img3.png,img4.png --layout grid
    python3 combine_panels.py --auto --prefix spring-campus --max 5
"""

import argparse
import json
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# 目录配置
TEMPLATE_DIR = Path(__file__).parent.resolve()
SKILL_DIR = TEMPLATE_DIR.parent.parent  # skill 根目录
CONFIG_FILE = SKILL_DIR / "config.json"
DEFAULT_OUTPUT_DIR = "~/.hermes/output/gpt-image-2"


def resolve_output_dir():
    """从 config.json 读取 output_dir，返回 video-pitch 模板子目录。"""
    import json
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    except Exception:
        config = {}
    base = Path(config.get('output_dir', DEFAULT_OUTPUT_DIR)).expanduser()
    return base / "video-pitch"

# 拼接配置
BACKGROUND_COLOR = (20, 20, 30)  # 深色背景
SPACING = 20  # 图片间距
LABEL_HEIGHT = 40  # 标签高度
LABEL_FONT_SIZE = 24


def load_images(image_paths):
    """加载图片列表"""
    images = []
    for path in image_paths:
        full_path = resolve_output_dir() / path if not Path(path).exists() else Path(path)
        if full_path.exists():
            img = Image.open(full_path)
            images.append(img)
        else:
            print(f"Warning: Image not found: {path}")
    return images


def create_label(text, width, height=LABEL_HEIGHT):
    """创建标签图片"""
    label = Image.new('RGB', (width, height), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(label)
    
    # 尝试加载字体
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", LABEL_FONT_SIZE)
    except:
        try:
            # macOS fallback
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", LABEL_FONT_SIZE)
        except:
            try:
                # Windows fallback
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", LABEL_FONT_SIZE)
            except:
                # 最终 fallback
                font = ImageFont.load_default()
                print("Warning: Using default font, custom fonts not available")
    
    # 绘制文字（居中）
    text_width = len(text) * LABEL_FONT_SIZE // 2
    x = (width - text_width) // 2
    y = (height - LABEL_FONT_SIZE) // 2
    draw.text((x, y), text, fill=(255, 215, 0), font=font)  # 金色文字
    
    return label


def combine_vertical(images, labels=None):
    """垂直拼接（竖向）"""
    if not images:
        return None
    
    # 计算总高度
    total_height = sum(img.height for img in images) + SPACING * (len(images) - 1)
    max_width = max(img.width for img in images)
    
    # 添加标签高度
    if labels:
        total_height += LABEL_HEIGHT * len(labels) + SPACING * len(labels)
    
    # 创建画布
    canvas = Image.new('RGB', (max_width, total_height), BACKGROUND_COLOR)
    
    y_offset = 0
    for i, img in enumerate(images):
        # 添加标签
        if labels and i < len(labels):
            label = create_label(labels[i], max_width)
            canvas.paste(label, (0, y_offset))
            y_offset += LABEL_HEIGHT + SPACING
        
        # 居中放置图片
        x_offset = (max_width - img.width) // 2
        canvas.paste(img, (x_offset, y_offset))
        y_offset += img.height + SPACING
    
    return canvas


def combine_horizontal(images, labels=None):
    """水平拼接（横向）"""
    if not images:
        return None
    
    # 计算总宽度
    total_width = sum(img.width for img in images) + SPACING * (len(images) - 1)
    max_height = max(img.height for img in images)
    
    # 创建画布
    canvas = Image.new('RGB', (total_width, max_height), BACKGROUND_COLOR)
    
    x_offset = 0
    for i, img in enumerate(images):
        # 垂直居中
        y_offset = (max_height - img.height) // 2
        canvas.paste(img, (x_offset, y_offset))
        x_offset += img.width + SPACING
    
    return canvas


def combine_grid(images, cols=2, labels=None):
    """网格拼接"""
    if not images:
        return None
    
    rows = (len(images) + cols - 1) // cols
    
    # 计算网格尺寸
    cell_width = max(img.width for img in images)
    cell_height = max(img.height for img in images)
    
    # 添加标签空间
    cell_height += LABEL_HEIGHT if labels else 0
    
    total_width = cols * cell_width + (cols - 1) * SPACING
    total_height = rows * cell_height + (rows - 1) * SPACING
    
    # 创建画布
    canvas = Image.new('RGB', (total_width, total_height), BACKGROUND_COLOR)
    
    for i, img in enumerate(images):
        row = i // cols
        col = i % cols
        
        x_offset = col * (cell_width + SPACING)
        y_offset = row * (cell_height + SPACING)
        
        # 添加标签
        if labels and i < len(labels):
            label = create_label(labels[i], cell_width)
            canvas.paste(label, (x_offset, y_offset))
            y_offset += LABEL_HEIGHT + SPACING // 2
        
        # 居中放置图片
        img_x = x_offset + (cell_width - img.width) // 2
        img_y = y_offset + (cell_height - LABEL_HEIGHT - img.height) // 2
        canvas.paste(img, (img_x, img_y))
    
    return canvas


def auto_combine(prefix, max_count=5):
    """自动查找并拼接前缀匹配的图片"""
    matching_files = sorted(resolve_output_dir().glob(f"{prefix}*.png"))
    
    if not matching_files:
        print(f"No images found with prefix: {prefix}")
        return None
    
    # 限制数量
    images = []
    for f in matching_files[:max_count]:
        img = Image.open(f)
        images.append(img)
        print(f"  Found: {f.name}")
    
    if len(images) == 0:
        return None
    elif len(images) == 1:
        return images[0]
    elif len(images) == 2:
        return combine_vertical(images, ["Part 1", "Part 2"])
    else:
        # 多图使用网格布局
        labels = [f"Part {i+1}" for i in range(len(images))]
        cols = 2 if len(images) <= 4 else 3
        return combine_grid(images, cols, labels)


def main():
    parser = argparse.ArgumentParser(
        description="video-pitch / combine_panels：拼接多张 panel 图片（图片读取/输出都基于 ~/.hermes/output/gpt-image-2/video-pitch/）"
    )
    parser.add_argument("--images", type=str, help="图片路径列表（逗号分隔）")
    parser.add_argument("--layout", type=str, default="vertical", 
                       choices=["vertical", "horizontal", "grid"],
                       help="拼接布局方式")
    parser.add_argument("--cols", type=int, default=2, help="网格列数（grid模式）")
    parser.add_argument("--labels", type=str, help="标签列表（逗号分隔）")
    parser.add_argument("--output", type=str, default="combined.png", help="输出文件名")
    parser.add_argument("--timeout", type=int, default=500, help="保留统一接口风格；拼接脚本本身不发起网络请求")
    parser.add_argument("--auto", action="store_true", help="自动模式：查找前缀匹配的图片")
    parser.add_argument("--prefix", type=str, help="自动模式：图片前缀")
    parser.add_argument("--max", type=int, default=5, help="自动模式：最大图片数量")
    
    args = parser.parse_args()
    
    if args.auto and args.prefix:
        # 自动模式
        result = auto_combine(args.prefix, args.max)
    elif args.images:
        # 手动模式
        image_paths = args.images.split(",")
        images = load_images(image_paths)
        
        labels = None
        if args.labels:
            labels = args.labels.split(",")
        
        if args.layout == "vertical":
            result = combine_vertical(images, labels)
        elif args.layout == "horizontal":
            result = combine_horizontal(images, labels)
        elif args.layout == "grid":
            result = combine_grid(images, args.cols, labels)
        else:
            result = combine_vertical(images, labels)
    else:
        print("Error: Need --images or --auto --prefix")
        sys.exit(1)
    
    if result:
        output_path = resolve_output_dir() / args.output
        result.save(output_path, "PNG")
        print(f"Combined image saved: {output_path}")
        print(f"Size: {result.width}x{result.height}")
    else:
        print("Error: No images to combine")


if __name__ == "__main__":
    main()
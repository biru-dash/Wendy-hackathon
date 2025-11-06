# Image Sizing Note

All PNG diagram images should be standardized to the same dimensions for consistent presentation.

## Recommended Size

- **Width**: 1200px
- **Height**: Auto (maintain aspect ratio)
- **Format**: PNG with transparent background (if possible)

## How to Standardize Images

### Using ImageMagick

```bash
# Windows (if ImageMagick installed)
magick convert input.png -resize 1200x output.png

# Mac/Linux
convert input.png -resize 1200x output.png
```

### Using Python (PIL/Pillow)

```python
from PIL import Image

def resize_image(input_path, output_path, target_width=1200):
    img = Image.open(input_path)
    aspect_ratio = img.height / img.width
    target_height = int(target_width * aspect_ratio)
    resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    resized.save(output_path, 'PNG')

# Resize all images
images = [
    'overall-agent-system-design.png',
    'market-trends-analyst.png',
    'customer-insights.png',
    'offer-design.png',
    'marketing-orchestrator.png'
]

for img in images:
    resize_image(img, img, target_width=1200)
```

### Using Online Tools

1. Use an online image resizer like https://www.iloveimg.com/resize-image
2. Set width to 1200px
3. Maintain aspect ratio
4. Download and replace the original files

## Current Images

All images are located in `docs/mermaid_diagrams/`:
- `overall-agent-system-design.png`
- `market-trends-analyst.png`
- `customer-insights.png`
- `offer-design.png`
- `marketing-orchestrator.png`

## Note for PDF Conversion

When converting to PDF, ensure all images are the same size to maintain visual consistency. The images are referenced in `docs/hackathon_agenda.md` and should display at consistent sizes.


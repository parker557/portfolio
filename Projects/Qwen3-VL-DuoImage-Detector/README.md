# Qwen3-VL Batch Matching & Detection Script User Guide

## Overview

This script is designed for the "find similar by image" task using paired images: based on a reference image (the target object), it detects all objects of the same class within a test image (which may contain multiple similar objects). It outputs bounding boxes and supports visual rendering as well as CSV exporting.

## Core Features

* **Auto-Pairing**: Intelligently matches `test<ID>` with `test<ID>_ref` image files.
* **Batch Inference**: Utilizes the Qwen3-VL-8B-Instruct model for batch processing.
* **Multi-Format Output**:
* Visualized images: `output/test<ID>_result.jpg`
* JSON results: `output/test<ID>_results.json`
* CSV summaries: `csv_output/batch_results*.csv`


* **State Memory**: Records the CSV path to facilitate append writing.
* **Performance Benchmarking**: Supports multi-epoch timing tests.
* **Scene-Customized Prompts**: Supports appending numbered scene entries to the prompt via a scene file.
* **Model Path Caching**: Interactively prompts for input on the first run if no cache exists; automatically caches upon successful loading, bypassing the need for input in subsequent runs.

## Directory Structure

```text
project/
├─ qwen3_8b_test2.py          # Main script
├─ input/                     # Input directory
│  ├─ test1.jpg               # Test image (Search area)
│  ├─ test1_ref.jpg           # Reference image (Target object)
│  ├─ test2.png
│  └─ test2_ref.png
├─ output/                    # Inference output (Visualizations)
├─ csv_output/                # CSV output
└─ ...

```

## Quick Start

### Environment Setup

```bash
# Create a conda environment
conda create -n jiang-test python=3.12 -y
conda activate jiang-test

# Install dependencies
pip install torch pillow transformers openpyxl
# Install qwen-vl-utils (depending on your actual setup)

```

Or using `environment.yml`:

```yaml
conda env create -f environment.yml -n jiang-test

```

### Basic Usage

```bash
python qwen3_8b_test2.py \
  --input_dir input \
  --output_dir output \
  --csv_dir csv_output

```

During execution, it will sequentially prompt:

* Whether to append to the CSV (default `y`)
* Whether to perform a performance test (default `n`)
* The number of epochs for the performance test (default `5`, if the performance test is selected)

> **Regarding Model Path (New Caching Logic)**
> * If `--model_path` is **not specified** in the command line: The script will first attempt to read the cached path (`~/.qwen3_vl_batch_cache.json`).
> * If there is **no cache or the cache is invalid**: You will be prompted to **interactively input** the local model path. If the input is empty, the path doesn't exist, or loading fails, the script will report an error, exit, and **will not write to the cache**.
> * Once the model is **successfully loaded**, the path will automatically be written to/refresh the cache.
> * You can also explicitly specify it at any time using `--model_path`. Upon successful loading, it will overwrite the cache.
> 
> 

### Scene-Customized Prompts (New)

* By default, the script uses the **default prompt** or the custom prompt passed via `--prompt`.
* The **scene prompt file** is only enabled **when explicitly provided** via `--scene_file <txt_path>`:
* The file should contain one "special scene description" per line:
```text
<Special scene description>
<Special scene description>
<Special scene description>

```


* Once enabled, the final prompt will **append numbered scene entries** (1. / 2. / 3. ...) after the main instructional paragraph.
* If the file specified by `--scene_file` **does not exist or is empty**, the script will **report an error and exit**.



Example:

```bash
# Use the default prompt (or combined with --prompt)
python qwen3_8b_test2.py

# Use the scene prompt file (will automatically load and generate a prompt with numbered entries)
python qwen3_8b_test2.py --scene_file special_bat.txt

```

> Prompt template snippet (numbered entries will be appended when the scene file is enabled):
> ```text
> Based on the two images above. The first image shows a target object. The second image contains multiple target objects.
> Please analyze the target object in the first image, then find all objects of the same type in the second image, and output a bounding box for each detected object.
> Please only return JSON, do not include extra explanations, prefixes/suffixes, or Markdown code blocks, and uniformly use "target_object" for the label.
> 
> ```
> 
> 

> 1.
> 2.
> 3.

> JSON Format (example values are for structural reference only):
> {
> "results": [
> { "bbox": [480,365,610,440], "label": "target_object" },
> { "bbox": [580,375,775,480], "label": "target_object" }
> ]
> }
> ```
> 
> ```
> 
> 

## Parameters

| Parameter | Default Value | Description |
| --- | --- | --- |
| `--model_path` | `""` (Unspecified) | Local model path. If left empty, it reads the cache or prompts for input; caches upon successful load. |
| `--input_dir` | `input` | Input image directory |
| `--output_dir` | `output` | Visualized output directory |
| `--csv_dir` | `csv_output` | CSV output directory |
| `--prompt` | Default Prompt | Text prompt used when `--scene_file` is not specified. |
| `--scene_file` | `""` (Disabled) | TXT file path for scene prompts. **Enabled only if explicitly provided**; exits on error if missing or empty. |
| `--attn_impl` | `flash_attention_2` | Attention implementation: `flash_attention_2` / `sdpa` / `eager` |

## Default Prompt

```text
Based on the two images above. The first image shows a target object. The second image contains multiple target objects.
Please analyze the target object in the first image, then find all objects of the same type in the second image, and output a bounding box for each detected object.
Please only return JSON, do not include extra explanations, prefixes/suffixes, or Markdown code blocks, and uniformly use "target_object" for the label.

```

Expected Output Format:

```json
{
  "results": [
    { "bbox": [x1, y1, x2, y2], "label": "target_object", "score": optional }
  ]
}

```

## Output Files Description

### 1. Visualized Images

* Path: `output/test<ID>_result.jpg`
* Visualized results containing the drawn bounding boxes and labels.

### 2. JSON Result Files

```json
{
  "results": [
    {
      "label": "target_object",
      "bbox_qwen1000": [480.0, 365.0, 610.0, 440.0],
      "bbox_2d": [xmin, ymin, xmax, ymax],
      "score": 0.95
    }
  ]
}

```

### 3. CSV Summary Files

Included fields:

* `Reference Input Image Path`
* `Reference Input Image Size (H*W)`
* `Input Image Path`
* `Input Image Size (H*W)`
* `Inference Result (Records the first result only)`
* `Inference Time (Average time)`
* `Prompt`

## Technical Implementation

### Key Workflows

1. **Pairing Collection**: Precisely matches `testN` and `testN_ref` files.
2. **Input Construction**: Text → Reference Image → Text → Test Image → Prompt.
3. **Inference & Parsing**: Supports JSON extraction and error handling.
4. **Coordinate Conversion**: Converts from normalized coordinates (0–1000) to pixel coordinates.
5. **Result Saving**: Multi-format outputs for Visualization, JSON, and CSV.

### File Pairing Rules

* Supported formats: `.jpg/.jpeg/.png/.bmp/.webp/.tif/.tiff`
* Test image: `test<ID>.<extension>`
* Reference image: `test<ID>_ref.<extension>`

## FAQ

**Q: Prompting "Unpaired images found" error.**
A: Ensure that the `testN` and `testN_ref` files have matching ID numbers and both exist.

**Q: The model output is not pure JSON.**
A: The script automatically extracts the valid JSON portion and supports parsing ```json code blocks.

**Q: Out of VRAM (OOM) or slow speeds.**
A: Try the following:

* Switch `--attn_impl` to `sdpa` or `eager`.
* Lower the image resolution.
* Ensure `flash-attn` is correctly installed and enabled.

**Q: Conditions for the Scene File to take effect (New).**
A: It is only enabled when `--scene_file` is explicitly provided. The script will error and exit if the file is empty or missing. If not provided, `--prompt` (or the default prompt) is used.

**Q: Model path caching rules (New).**
A: It only writes to `~/.qwen3_vl_batch_cache.json` after a successful load. Providing `--model_path` overrides and refreshes the cache. If loading fails or the input is empty/invalid, it exits directly without writing to the cache.

## Utilities

### CSV to Excel Tool

```bash
# Batch conversion (non-recursive)
python csv2xlsx.py --input-dir ./csv_output --output-dir ./xlsx_output --autowidth

# Batch conversion (recursive)
python csv2xlsx.py -I ./csv_output -O ./xlsx_output -R --autowidth

# Single file conversion
python csv2xlsx.py -i ./csv_output/batch_results.csv -o ./xlsx_output/batch_results.xlsx --autowidth

```

## Example Workflow

```bash
# 1. Prepare test images
mkdir -p input
cp demo_a.jpg input/test1.jpg
cp demo_a_crop.jpg input/test1_ref.jpg

# 2. Run detection (reads cache or prompts for interactive input if --model_path is unspecified on the first run)
python qwen3_8b_test2.py --input_dir input --output_dir output --csv_dir csv_output

# Or explicitly specify the model to refresh the cache
python qwen3_8b_test2.py --model_path /models/Qwen3-VL-8B-Instruct \
  --input_dir input --output_dir output --csv_dir csv_output

# 3. View results
ls output/ csv_output/

```

## Keywords

### Features / Tasks

以图找同类、以图搜图、参考图匹配、同类目标检测、目标定位、边界框标注、批量标注、可视化标注、CSV导出
image-based matching, reference-based detection, same-class detection, object localization, bounding box annotation, batch annotation, visualization, CSV export

### Prompts / Interaction

照片+提示词标注、基于提示词的检测、文本驱动检测、场景化提示词、可定制提示词、编号场景提示词
prompt-guided detection, text-prompted detection, scene prompts, customizable prompts, prompt engineering for vision

### Multimodal / Model Related

多模态视觉、视觉语言模型、Qwen3-VL、Qwen3-VL-8B-Instruct、开源大模型、本地推理
multimodal vision, vision-language model, VLM, Qwen3-VL, local inference, offline inference

### Technical (Search / Academic)

视觉指引、视觉对齐、视觉定位、跨图检索、特征相似度、归一化坐标、像素坐标转换、可重复试验
visual grounding, referring image, cross-image retrieval, similarity matching, normalized coords, pixel conversion, reproducibility

### Engineering / Pipeline

自动配对、批处理、性能评测、显存优化、Flash-Attn、SDPA、可配置参数、模型路径缓存、状态文件、日志
auto pairing, batch processing, benchmarking, memory optimization, flash attention, SDPA, configurable params, model path cache, state file, logging

### Typical Scenarios (Long-tail Search Queries)

“以照片输入提示词的方式标注照片”
“参考图引导在大图中找相同物体”
“批量将归一化坐标转换为像素并可视化”
“用Qwen3-VL做以图找同类并输出bbox”
“场景化提示词驱动的目标检测批处理”
“本地多模态模型的离线批量标注管线”
"Photo-to-Prompt Annotation"
"Reference-Guided Object Localization"
"Batch Normalized-to-Pixel Coordinate Conversion"
"Qwen3-VL Visual Retrieval with BBox Output"
"Context-Aware Batch Object Detection"
"Local Multimodal Batch Annotation Pipeline"

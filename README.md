# Auto Lip Sync Plugin for Maya

Multi-language lip sync plugin supporting English and Chinese using Montreal Forced Aligner (MFA).

## Quick Start
1. **Clone this repository**
2. **Download required models** (see "Required Downloads" section below)
3. **Install MFA environment** (see "Setup" section)
4. **Load plugin in Maya** and start creating lip sync animations!

> **Note:** This repository contains only the plugin code and small sample files. Large MFA models must be downloaded separately.

## 🚀 Portable Installation (Recommended)
For easy deployment without conda dependencies:

1. **Run portable setup:**
   ```bash
   python portable_setup.py
   ```

2. **Download required models** (see "Required Downloads" section)

3. **Copy entire folder** to any location - it's now self-contained!

> **Portable Benefits:** No conda required, works on any system with Python 3.11+, easy to distribute

## Setup

### 1. Install MFA Environment
```bash
# Create conda environment
conda create -n mfa-323 python=3.11
conda activate mfa-323

# Install MFA 3.2.3 and dependencies
conda install -c conda-forge montreal-forced-aligner=3.2.3
conda install -c conda-forge openfst
pip install spacy-pkuseg dragonmapper hanziconv

# Add openfst to PATH (Windows)
set PATH=%CONDA_PREFIX%\Library\bin;%PATH%
```

**📥 Alternative Installation Methods:**
- **From Source:** [MFA 3.2.3 Source Code](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/tag/v3.2.3)
- **Conda Package:** `conda install -c conda-forge montreal-forced-aligner=3.2.3`
- **Pip Package:** `pip install montreal-forced-aligner==3.2.3`

### 2. Download Required Models and Dictionaries

**⚠️ Version Information:**
- **MFA Software Version:** 3.2.3 (this is what we install)
- **Dictionary Version:** 3.0.0 (compatible with MFA 3.2.3)
- **Acoustic Model Version:** 3.0.0 (compatible with MFA 3.2.3)

**English Models:**
- Download [Librispeech English Lexicon](https://www.openslr.org/resources/11/librispeech-lexicon.txt) and place it in your project root as `librispeech-lexicon.txt`

**Chinese Models:**
- Download [Mandarin Chinese Dictionary](https://github.com/MontrealCorpusTools/mfa-models/releases/download/dictionary-mandarin_china_mfa-v3.0.0/mandarin_china_mfa3.0.0.dict) and place it in `MFA_3.2.3/` folder
- Download [Mandarin Chinese Acoustic Model](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-mandarin_mfa-v3.0.0/mandarin_mfa%20v3.0.0.zip) and place it in `MFA_3.2.3/` folder

### 3. Test Alignment
```bash
# Test with sample files
python -m montreal_forced_aligner.command_line.mfa align Speaker_1 MFA_3.2.3/mandarin_china_mfa3.0.0.dict "MFA_3.2.3/mandarin_mfa v3.0.0.zip" test_output
```

## Usage

1. Load the plugin in Maya
2. Select language (English/Chinese)
3. Input audio file and transcript
4. Run alignment
5. Apply to character animation

## File Structure
- `auto_lip_sync/` - Maya plugin code
- `Sample_Audio/` - Test audio files (small examples included)
- `Sample_Text/` - Test transcript files
- `Speaker_1/` - Proper corpus structure for MFA

## Required Downloads (Not Included in Repository)
Due to size constraints, the following files need to be downloaded separately:

### Create these folders and download files:
```
MFA_3.2.3/
├── mandarin_china_mfa3.0.0.dict     # Download from MFA models
└── mandarin_mfa v3.0.0.zip          # Download from MFA models

Root directory:
└── librispeech-lexicon.txt          # Download from OpenSLR
```

**Download Links:**
- [Librispeech English Lexicon](https://www.openslr.org/resources/11/librispeech-lexicon.txt)
- [Mandarin Chinese Dictionary](https://github.com/MontrealCorpusTools/mfa-models/releases/download/dictionary-mandarin_china_mfa-v3.0.0/mandarin_china_mfa3.0.0.dict)
- [Mandarin Chinese Acoustic Model](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-mandarin_mfa-v3.0.0/mandarin_mfa%20v3.0.0.zip)

**📋 Version Summary:**
```
MFA Software: 3.2.3 ✅
Dictionary: mandarin_china_mfa3.0.0.dict ✅  
Acoustic Model: mandarin_mfa v3.0.0 ✅
```

# Automated lip sync tool for Maya

Inspired by " https://github.com/joaen/maya-auto-lip-sync "


 A tool used for generating automated lip sync animation on a facial rig in Autodesk: Maya. The script is compatible with Autodesk: Maya 2017 or later (Windows).

 ![](https://joaen.github.io/images/auto-lip-sync.gif)

## Installation:
1. Add the ***auto_lip_sync*** folder or ***auto_lip_sync.py*** to your Maya scripts folder (Username\Documents\maya\*version*\scripts).
2. Install the dependencies needed to run this tool. (Read the *Dependencies* section further down).
3. To start the auto lipsync tool in Maya simply execute the following lines of code in the script editor or add them as a shelf button:

```python
import auto_lip_sync
auto_lip_sync.start()
```

## Dependencies
To be able to run this tool you need to download the dependencies which are required to run this tool (Or move the *INSTALLER.bat* to your Maya scripts folder and run it).

* Montreal Forced Aligner version 1.0.1 Win64, by Michael McAuliffe/Montreal Corpus Tools (MIT/Apache). Unzip this folder in your Maya scripts folder:
https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/download/v1.0.1/montreal-forced-aligner_win64.zip

* Textgrid parser by Kyle Gorman (MIT). Download and move the textgrid folder to your Maya scripts folder:
https://github.com/kylebgorman/textgrid

* Librispeech English pronunciations by Daniel Povey/OpenSLR (Public Domain). Download and place this file inside your montreal-forced-aligner folder:
https://www.openslr.org/resources/11/librispeech-lexicon.txt


## System and file format requirements
* This tool only have support for English input sound and text files.
* Maya 2017+ and Windows is required to run this tool.
* Input transcript file have to be a .txt file or .lab file.
* Input sound file only have support for 16 kHz, single channel .Wav files. You may need to resample your sound file to meet the requirements. I recommend using the free and open-source software Audacity: https://www.audacityteam.org/ 

## How to use the tool

### English
1. Use the *Save pose* function to create 10 separate facial poses (one for each phoneme). 
2. Load the folder where the pose files are saved and assign a unique pose to each phoneme in the dropdown boxes.
3. Select a soundclip with a voice-line and a textfile where the voice-line is written down in English.
4. Click *Generate animation* and wait until the process is done. (The length of the audio clip will affect how long it takes to process)

### Chinese (中文)
1. 使用 *Save pose* 功能创建10个独立的面部Pose（每个音素一个）。
2. 加载保存Pose文件的文件夹，并在下拉框中为每个音素分配唯一的Pose。
3. 选择包含语音的音频文件和用中文书写的语音文本文件。
4. 点击 *Generate animation* 并等待处理完成。（音频文件的长度会影响处理时间）

## Preston Blair phoneme series
To be able to generate facial animations you need to create 10 different mouth poses based on the Preston Blair phoneme series.

![](https://i.imgur.com/vpm7DEr.jpg)

## How to save a pose
1. Select the rig controllers you wish to save the attributes from.
2. Click *Save pose* and choose which path you want to save the pose file to.

## How to load a pose
1. Click *Load pose* and select which pose file you wish to load.
2. The stored pose will be applied to the rig controllers referenced in the pose file.

---

# Maya 自动唇形同步插件

支持英语和中文的多语言唇形同步插件，使用蒙特利尔强制对齐器 (MFA)。

## 快速开始
1. **克隆此仓库**
2. **下载所需模型**（见下方"必需下载"部分）
3. **安装 MFA 环境**（见"安装"部分）
4. **在 Maya 中加载插件**并开始创建唇形同步动画！

> **注意：** 此仓库仅包含插件代码和小型示例文件。大型 MFA 模型需要单独下载。

## 🚀 便携式安装（推荐）
为了便于部署而无需 conda 依赖：

1. **运行便携式设置：**
   ```bash
   python portable_setup.py
   ```

2. **下载所需模型**（见"必需下载"部分）

3. **复制整个文件夹**到任何位置 - 现在它是自包含的！

> **便携式优势：** 无需 conda，适用于任何 Python 3.11+ 系统，易于分发

## 安装

### 1. 安装 MFA 环境
```bash
# 创建 conda 环境
conda create -n mfa-323 python=3.11
conda activate mfa-323

# 安装 MFA 3.2.3 和依赖
conda install -c conda-forge montreal-forced-aligner=3.2.3
conda install -c conda-forge openfst
pip install spacy-pkuseg dragonmapper hanziconv

# 将 openfst 添加到 PATH（Windows）
set PATH=%CONDA_PREFIX%\Library\bin;%PATH%
```

**📥 其他安装方法：**
- **从源码：** [MFA 3.2.3 源码](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/tag/v3.2.3)
- **Conda 包：** `conda install -c conda-forge montreal-forced-aligner=3.2.3`
- **Pip 包：** `pip install montreal-forced-aligner==3.2.3`

### 2. 下载所需模型和词典

**⚠️ 版本信息：**
- **MFA 软件版本：** 3.2.3（这是我们安装的）
- **词典版本：** 3.0.0（与 MFA 3.2.3 兼容）
- **声学模型版本：** 3.0.0（与 MFA 3.2.3 兼容）

**英语模型：**
- 下载 [Librispeech 英语词典](https://www.openslr.org/resources/11/librispeech-lexicon.txt) 并将其放在项目根目录中作为 `librispeech-lexicon.txt`

**中文模型：**
- 下载 [普通话中文词典](https://github.com/MontrealCorpusTools/mfa-models/releases/download/dictionary-mandarin_china_mfa-v3.0.0/mandarin_china_mfa3.0.0.dict) 并将其放在 `MFA_3.2.3/` 文件夹中
- 下载 [普通话中文声学模型](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-mandarin_mfa-v3.0.0/mandarin_mfa%20v3.0.0.zip) 并将其放在 `MFA_3.2.3/` 文件夹中

### 3. 测试对齐
```bash
# 使用示例文件测试
python -m montreal_forced_aligner.command_line.mfa align Speaker_1 MFA_3.2.3/mandarin_china_mfa3.0.0.dict "MFA_3.2.3/mandarin_mfa v3.0.0.zip" test_output
```

## 使用方法

1. 在 Maya 中加载插件
2. 选择语言（英语/中文）
3. 输入音频文件和转录文本
4. 运行对齐
5. 应用到角色动画

## 文件结构
- `auto_lip_sync/` - Maya 插件代码
- `Sample_Audio/` - 测试音频文件（包含小示例）
- `Sample_Text/` - 测试转录文件
- `Speaker_1/` - MFA 的正确语料库结构

## 必需下载（仓库中未包含）
由于大小限制，以下文件需要单独下载：

### 创建这些文件夹并下载文件：
```
MFA_3.2.3/
├── mandarin_china_mfa3.0.0.dict     # 从 MFA 模型下载
└── mandarin_mfa v3.0.0.zip          # 从 MFA 模型下载

根目录：
└── librispeech-lexicon.txt          # 从 OpenSLR 下载
```

**下载链接：**
- [Librispeech 英语词典](https://www.openslr.org/resources/11/librispeech-lexicon.txt)
- [普通话中文词典](https://github.com/MontrealCorpusTools/mfa-models/releases/download/dictionary-mandarin_china_mfa-v3.0.0/mandarin_china_mfa3.0.0.dict)
- [普通话中文声学模型](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-mandarin_mfa-v3.0.0/mandarin_mfa%20v3.0.0.zip)

**📋 版本摘要：**
```
MFA 软件：3.2.3 ✅
词典：mandarin_china_mfa3.0.0.dict ✅  
声学模型：mandarin_mfa v3.0.0 ✅
```

# Maya 自动唇形同步工具

用于在 Autodesk Maya 中的面部绑定上生成自动唇形同步动画的工具。该脚本兼容 Autodesk Maya 2017 或更高版本（Windows）。

原作 " https://github.com/joaen/maya-auto-lip-sync "

https://github.com/user-attachments/assets/45503cf4-28d0-4e19-a07f-318d37be69a1
https://github.com/user-attachments/assets/4933039e-7329-42b4-846d-392483cb7fd9

## 安装：
1. 将 ***auto_lip_sync*** 文件夹或 ***auto_lip_sync.py*** 添加到您的 Maya 脚本文件夹中（用户名\Documents\maya\*版本*\scripts）。
2. 安装运行此工具所需的依赖项。（阅读下面的*依赖项*部分）。
3. 要在 Maya 中启动自动唇形同步工具，只需在脚本编辑器中执行以下代码行或将其添加为架子按钮：

```python
import auto_lip_sync
auto_lip_sync.start()
```

## 依赖项
要能够运行此工具，您需要下载运行此工具所需的依赖项（或将 *INSTALLER.bat* 移动到您的 Maya 脚本文件夹并运行它）。

* Montreal Forced Aligner 版本 1.0.1 Win64，由 Michael McAuliffe/Montreal Corpus Tools（MIT/Apache）制作。将此文件夹解压到您的 Maya 脚本文件夹中：
https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/download/v1.0.1/montreal-forced-aligner_win64.zip

* Textgrid 解析器，由 Kyle Gorman（MIT）制作。下载并将 textgrid 文件夹移动到您的 Maya 脚本文件夹：
https://github.com/kylebgorman/textgrid

* Librispeech 英语发音，由 Daniel Povey/OpenSLR（公共领域）制作。下载并将此文件放在您的 montreal-forced-aligner 文件夹内：
https://www.openslr.org/resources/11/librispeech-lexicon.txt

## 系统和文件格式要求
* 此工具仅支持英语输入声音和文本文件。
* 需要 Maya 2017+ 和 Windows 才能运行此工具。
* 输入转录文件必须是 .txt 文件或 .lab 文件。
* 输入声音文件仅支持 16 kHz、单声道 .Wav 文件。您可能需要重新采样声音文件以满足要求。我推荐使用免费开源软件 Audacity：https://www.audacityteam.org/ 

## 如何使用工具

### 英语
1. 使用 *Save pose* 功能创建 10 个独立的面部Pose（每个音素一个）。
2. 加载保存Pose文件的文件夹，并在下拉框中为每个音素分配唯一的Pose。
3. 选择包含语音的音频文件和用英语书写的语音文本文件。
4. 点击 *Generate animation* 并等待处理完成。（音频文件的长度会影响处理时间）

### 中文（中文）
1. 使用 *Save pose* 功能创建 10 个独立的面部Pose（每个音素一个）。
2. 加载保存Pose文件的文件夹，并在下拉框中为每个音素分配唯一的Pose。
3. 选择包含语音的音频文件和用中文书写的语音文本文件。
4. 点击 *Generate animation* 并等待处理完成。（音频文件的长度会影响处理时间）

## Preston Blair 音素系列
要能够生成面部动画，您需要基于 Preston Blair 音素系列创建 10 种不同的嘴部Pose。

![](https://i.imgur.com/vpm7DEr.jpg)

## 如何保存Pose
1. 选择您希望保存属性的绑定控制器。
2. 点击 *Save pose* 并选择您希望保存Pose文件的路径。

## 如何加载Pose
1. 点击 *Load pose* 并选择您希望加载的Pose文件。
2. 存储的Pose将应用到Pose文件中引用的绑定控制器。


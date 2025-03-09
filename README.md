# 模式分析系统 (Pattern Analysis System)

本系统提供了一套综合解决方案，利用先进的语言模型分析文本模式并提取相关信息。

[English Version](README_EN.md)

## 概述 (Overview)

该工具旨在帮助：
- 检测重要模式
- 识别关键信息
- 分析文本内容
- 评估内容关系
- 监控变化和趋势

## 系统组件 (Components)

### 1. FastAPI 后端 (Backend)
- 专用于文本分析的API端点
- 使用LLaMA模型的高级模式识别
- 支持本地和远程处理

### 2. Streamlit 网页界面 (Web Interface)
- 文本分析的直观界面
- 实时高亮显示发现结果
- 交互式可视化
- 可配置参数

## 安装方法 (Installation)

1. 克隆仓库:
```bash
$ git clone <repository_url>
$ cd <repository_directory>
```

2. 创建并激活虚拟环境:
```bash
$ python -m venv venv
$ source venv/bin/activate  # Windows系统使用 `venv\Scripts\activate`
```

3. 安装后端依赖:
```bash
$ pip install -r requirements.txt
```

4. 安装前端依赖:
```bash
$ pip install -r web/requirements_web.txt
```

## 使用方法 (Usage)

1. 启动FastAPI后端:
```bash
$ uvicorn main:app --reload --port 8080
```

2. 启动Streamlit界面:
```bash
$ cd web
$ streamlit run frontend.py
```

3. 在浏览器中访问 `http://localhost:8501`

## 核心功能 (Key Features)

- **模式识别 (Pattern Recognition)**: 自动识别重要模式
- **内容分析 (Content Analysis)**: 突出显示相关信息
- **进度跟踪 (Progress Tracking)**: 分析随时间变化的情况
- **响应分析 (Response Analysis)**: 评估内容关系
- **交互式分析 (Interactive Analysis)**: 带有详细注释的实时可视化

## 分析类别 (Analysis Categories)

系统专注于检测:
1. **关键模式 (Key Patterns)**
   - 主要指标
   - 相关元素
   - 连接组件

2. **信息关系 (Information Relationships)**
   - 直接连接
   - 间接关系
   - 模式关联

3. **进度指标 (Progress Indicators)**
   - 变化模式
   - 发展指标
   - 趋势分析

4. **响应标记 (Response Markers)**
   - 模式变化
   - 效果指标
   - 进度评估

## 技术细节 (Technical Details)

### API 端点

#### POST /search_remote/
使用远程LLM服务分析文本中的模式。

##### 请求体:
```json
{
    "report": "您的文本内容",
    "api_url": "http://your-llm-service-url",
    "model_name": "llama-3.3-70b-instruct",
    "temperature": 0.85,
    "top_p": 0.3,
    "max_tokens": 2000
}
```

##### 响应:
```json
[
    {
        "keyword": "识别出的模式",
        "matches": "内容中匹配的文本"
    }
]
```

## 项目结构 (Project Structure)
```
app/
    models.py      - 数据模型
    utils.py       - 核心分析算法
    config.py      - 模型配置
    prompts.py     - LLM分析提示
web/
    frontend.py    - 交互式网页界面
    requirements_web.txt
main.py           - FastAPI应用
requirements.txt   - 后端依赖
```

## 注意事项 (Note)
本系统需要访问兼容的LLM服务。虽然配置为使用LLaMA模型，但可以适配其他语言模型。建议定期更新模式识别数据库以保持分析准确性。

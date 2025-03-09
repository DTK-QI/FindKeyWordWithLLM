# 模式分析系統 (Pattern Analysis System)

<div align="center">
  <img src="https://img.shields.io/badge/platform-ASP.NET%20Core%208.0-blue" alt="Platform">
  <img src="https://img.shields.io/badge/language-C%23-brightgreen" alt="Language">
  <img src="https://img.shields.io/badge/database-SQL%20Server-red" alt="Database">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</div>

本系統提供了一套綜合解決方案，利用先進的語言模型分析文本模式並提取相關信息。

[English Version](README_EN.md)

## 概述 (Overview)

該工具旨在幫助：
- 檢測重要模式
- 識別關鍵信息
- 分析文本內容
- 評估內容關係
- 監控變化和趨勢

## 系統組件 (Components)

### 1. FastAPI 後端 (Backend)
- 專用於文本分析的API端點
- 使用LLaMA模型的高級模式識別
- 支持本地和遠程處理

### 2. Streamlit 網頁介面 (Web Interface)
- 文本分析的直觀介面
- 實時高亮顯示發現結果
- 互動式可視化
- 可配置參數

## 安裝方法 (Installation)

1. 克隆倉庫:
```bash
$ git clone <repository_url>
$ cd <repository_directory>
```

2. 創建並激活虛擬環境:
```bash
$ python -m venv venv
$ source venv/bin/activate  # Windows系統使用 `venv\Scripts\activate`
```

3. 安裝後端依賴:
```bash
$ pip install -r requirements.txt
```

4. 安裝前端依賴:
```bash
$ pip install -r web/requirements_web.txt
```

## 使用方法 (Usage)

1. 啟動FastAPI後端:
```bash
$ uvicorn main:app --reload --port 8080
```

2. 啟動Streamlit界面:
```bash
$ cd web
$ streamlit run frontend.py
```

3. 在瀏覽器中訪問 `http://localhost:8501`

## 核心功能 (Key Features)

- **模式識別 (Pattern Recognition)**: 自動識別重要模式
- **內容分析 (Content Analysis)**: 突出顯示相關信息
- **響應分析 (Response Analysis)**: 評估內容關係
- **互動式分析 (Interactive Analysis)**: 帶有詳細註釋的實時可視化

## 分析類別 (Analysis Categories)

系統專注於檢測:
1. **關鍵模式 (Key Patterns)**
   - 主要指標
   - 相關元素
   - 連接組件

2. **信息關係 (Information Relationships)**
   - 直接連接
   - 間接關係
   - 模式關聯

## 技術細節 (Technical Details)

### API 端點

#### POST /search_remote/
使用遠程LLM服務分析文本中的模式。

##### 請求體:
```json
{
    "report": "您的文本內容",
    "api_url": "http://your-llm-service-url",
    "model_name": "llama-3.3-70b-instruct",
    "temperature": 0.85,
    "top_p": 0.3,
    "max_tokens": 2000
}
```

##### 響應:
```json
[
    {
        "keyword": "識別出的模式",
        "matches": "內容中匹配的文本"
    }
]
```

## 項目結構 (Project Structure)
```
app/
    models.py      - 數據模型
    utils.py       - 核心分析算法
    config.py      - 模型配置
    prompts.py     - LLM分析提示
web/
    frontend.py    - 互動式網頁界面
    requirements_web.txt
main.py           - FastAPI應用
requirements.txt   - 後端依賴
```

## 注意事項 (Note)
本系統需要訪問兼容的LLM服務。雖然配置為使用LLaMA模型，但可以適配其他語言模型。建議定期更新模式識別數據庫以保持分析準確性。

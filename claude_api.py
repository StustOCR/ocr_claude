import base64
from anthropic import Anthropic
import os

def encode_pdf_to_base64(pdf_path):
    """將 PDF 轉換為 base64 編碼"""
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode('utf-8')

def process_pdf(pdf_path, api_key):
    """使用 Claude API 處理 PDF 文件"""
    # 初始化 Anthropic 客戶端
    client = Anthropic(
        api_key=api_key,
        default_headers={
            "anthropic-beta": "pdfs-2024-09-25"
        }
    )
    
    # 將 PDF 轉換為 base64
    base64_pdf = encode_pdf_to_base64(pdf_path)
    
    # 建構系統提示 - 先放 PDF，再放文字請求
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "這是一份需要處理的 PDF 文件。"
                },
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": base64_pdf
                    }
                },
                {
                    "type": "text",
                    "text": "請讀取並分析上述 PDF 文件的內容，保持原始格式輸出。請維持文字的排版與換行。"
                }
            ]
        }
    ]
    
    # 呼叫 API
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=messages
    )
    
    return response.content[0].text

def main():
    # 從環境變數獲取 API 金鑰
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("請設定 ANTHROPIC_API_KEY 環境變數")
    
    # PDF 檔案路徑
    pdf_path = "5256.pdf"  # 請替換為您的 PDF 檔案路徑
    
    try:
        # 檢查檔案大小
        file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # 轉換為 MB
        if file_size > 32:
            raise ValueError(f"PDF 檔案大小 ({file_size:.1f}MB) 超過 32MB 限制")
            
        # 處理 PDF
        result = process_pdf(pdf_path, api_key)
        print("處理結果:")
        print(result)
        
        # 將結果儲存到檔案
        with open("pdf_result.txt", "w", encoding="utf-8") as f:
            f.write(result)
        
    except Exception as e:
        print(f"發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()
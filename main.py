from io import BytesIO

import requests
from bs4 import BeautifulSoup, NavigableString
from docx import Document
from docx.shared import Inches
from urllib.parse import urljoin
import os

# 1. 初始化
url = "https://lovenikki.fandom.com/wiki/V1:_Chapter_1_Arriving_the_Wheat_Field"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}
res = requests.get(url, headers=headers)
res.encoding = 'utf-8'


soup = BeautifulSoup(res.text, 'lxml')

# 2. 提取目标 div

content_div= soup.find('div',class_='mw-content-ltr mw-parser-output')

# 3. 创建 Word 文档

doc = Document()
doc.add_heading('提取内容', level=1)

# 遍历所有元素（按文档流顺序）
for element in content_div.children:
    print(element)
    # 忽略空白和纯文本
    if isinstance(element, NavigableString):
        continue

    if element.name == 'p' or element.name == 'span' or element.name == 'a':
        text = element.get_text(separator='',strip=True)

        doc.add_paragraph(text)
    # 处理图片
    elif element.name == 'img':
        img_src = element.get('src', '')
        if img_src and not img_src.endswith('.svg'):
            img_url = img_src if img_src.startswith('http') else urljoin(url, img_src)
            # 下载图片数据
            img_data = requests.get(img_url).content

            # 保存图片到本地
            img_path = os.path.join("images", os.path.basename(img_url))
            with open(img_path, 'wb') as f:
                f.write(img_data)

            # 插入图片（Word 插入）
            try:
                doc.add_picture(img_path, width=Inches(4))
            except:
                doc.add_paragraph(f"[图片: {img_url}]")

            # 加入图片 URL 到文档
            # doc.append(f"[图片] {img_url}")


    # 处理表格
    elif element.name == 'table':
        rows = []
        for row in element.find_all('tr'):
            cells = []
            for cell in row.find_all(['td', 'th']):
                text = cell.get_text(separator='',strip=True)

                imgs = cell.find_all('img')
                for img in imgs:
                    img_src = img.get('src', '')
                    if img_src:
                        img_url = img_src if img_src.startswith('http') else urljoin(url, img_src)

                        img_class = img.get('class', [])
                        if 'mw-file-element ls-is-cached lazyloaded' in img_class:

                            img_width = img.get('width', 50)  # 默认为 100（可以调整）
                            img_height = img.get('height', 28)
                        else:
                            img_width = 40  # 默认大小
                            img_height = 40

                        if img_url.startswith('data:image'):
                            print("⚠️ 跳过 base64 图片")
                            continue
                        img_data = requests.get(img_url).content
                        img_stream = BytesIO(img_data)

                        try:
                            doc.add_picture(img_stream, width=Inches(img_width / 100), height=Inches(img_height / 100))
                        except:
                            doc.add_paragraph(f"[图片: {img_url}]")

                cells.append(text if text else "[空]")

                doc.add_paragraph(" | ".join(cells))

            # 合并结果，保留原始顺序
doc.save('output.docx')
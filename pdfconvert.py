import pdfkit

html_name = "cv17594139.html"
pdf_name = "cv17594139.pdf"

options = {
                'encoding': 'UTF-8',
                'no-outline': None,
                'enable-local-file-access': None,
                'quiet': '',
                'load-media-error-handling': 'ignore',
                'load-error-handling': 'ignore',
                'enable-local-file-access': None,
                'custom-header': [('Accept-Encoding', 'gzip')]
            }

# 将HTML内容转换为PDF
pdfkit.from_file(html_name, pdf_name, options=options)
print("PDF文件已生成：", pdf_name)

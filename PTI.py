import os
import fitz
import re

def sanitize_filename(name):
    """清理文件名中的非法字符"""
    return re.sub(r'[\\/*?:"<>|]', '_', name)

def pdf_to_images(input_folder, output_folder):
    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    # 遍历PDF文件夹
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]
            clean_name = sanitize_filename(base_name)

            try:
                # 打开PDF文件
                doc = fitz.open(pdf_path)
                print(f"正在处理: {filename} (共 {len(doc)} 页)")

                # 逐页转换为图片
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    pix = page.get_pixmap(dpi=300)
                    
                    # 生成文件名
                    output_path = os.path.join(
                        output_folder, 
                        f"{clean_name}_{page_num + 1}.jpg"
                    )
                    
                    # 保存图片
                    pix.save(output_path)
                    print(f"已保存: {os.path.basename(output_path)}")

            except Exception as e:
                print(f"处理 {filename} 失败: {str(e)}")
                continue

if __name__ == "__main__":
    # 自动获取当前脚本所在目录
    script_dir = os.path.dirname(__file__)
    
    # 设置相对路径
    input_folder = os.path.join(script_dir, "需要转换文件")    # 输入文件夹
    output_folder = os.path.join(script_dir, "全部转换完成")   # 输出文件夹
    
    # 验证输入文件夹存在
    if not os.path.exists(input_folder):
        print(f"错误：输入文件夹不存在，请在程序目录下创建 '{os.path.basename(input_folder)}' 文件夹")
    else:
        pdf_to_images(input_folder, output_folder)
        print("全部转换完成！")
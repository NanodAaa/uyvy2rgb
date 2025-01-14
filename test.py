import numpy as np

def get_yuv_image_dimensions(file_path):
    # 打开YUV文件
    with open(file_path, 'rb') as f:
        # 读取整个文件内容
        yuv_data = f.read()

    # 获取文件的总字节数
    file_size = len(yuv_data)

    # 计算图像的宽度和高度
    # UYVY格式每四个字节代表两个像素
    # 每两个Y分量占两个字节，每个U、V分量占一个字节
    # 图像的像素数量是文件大小除以4
    num_pixels = file_size // 4

    # 假设图像的宽度是1920，计算高度
    width = 1920  # 可以根据实际情况调整宽度
    height = num_pixels // width  # 高度是像素数除以宽度

    return width, height

# 示例用法
file_path = r'D:\NanodAaa\WORK\EM728\EM728\EM728_RGB彩条.yuv'  # 需要处理的YUV文件路径
width, height = get_yuv_image_dimensions(file_path)
print(f"图像的宽度: {width}, 高度: {height}")

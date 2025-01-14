import numpy as np

# 设置图像的宽和高
width = 640
height = 480

# 创建一个包含红色的UYVY数据
uyvy_data = np.zeros((height, width, 2), dtype=np.uint8)

# 填充数据，红色的UYVY分量：U = 0, Y = 76, V = 255
for i in range(height):
    for j in range(width):
        # 每个像素的UYVY值：U, Y, V, Y
        uyvy_data[i, j] = [0, 76, 255]  # U, Y, V

# 将数据保存为文件
uyvy_data = uyvy_data.flatten()
with open('red_image.uyvy', 'wb') as f:
    f.write(uyvy_data.tobytes())

print("红色UYVY文件生成成功！")

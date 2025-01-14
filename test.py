import numpy as np
import matplotlib.pyplot as plt

# 加载 .npy 文件
file_path = r"D:\NanodAaa\WORK\EM728\rgbdata_3d.npy"
array = np.load(file_path)

# 显示二维数组或图像
plt.imshow(array, cmap="gray")  # cmap 可根据需要选择，如 'gray', 'viridis'
plt.colorbar()  # 显示颜色条（可选）
plt.show()

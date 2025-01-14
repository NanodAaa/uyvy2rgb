import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm   # pip install

def read_uyvy(file_path): 
    if (not os.path.exists(os.path.join(FILE_DIRNAME, 'Y.txt'))) or (not os.path.exists(os.path.join(FILE_DIRNAME, 'U.txt'))) or (not os.path.exists(os.path.join(FILE_DIRNAME, 'V.txt'))):
        with open(file_path, 'rb') as f:
            raw_data = f.read()
    #        print(raw_data)
            yuv_data = np.frombuffer(raw_data, np.uint8)
    #        print(yuv_data)
        
        Y = np.zeros((Y_HEIGHT, Y_WIDTH), dtype=np.uint8)
        U = np.zeros((UV_HEIGHT, UV_WIDTH), dtype=np.uint8)
        V = np.zeros((UV_HEIGHT, UV_WIDTH), dtype=np.uint8)
        
        for i in tqdm(range(Y_SIZE), desc='Processing Y', ncols=100):
#        for i in range(Y_SIZE):
            y_index = i * 2 + 1
            Y[i // Y_WIDTH, i % Y_WIDTH] = raw_data[y_index]
            
        for i in tqdm(range(UV_SIZE), desc='Processing UV', ncols=100):
#        for i in range(UV_SIZE):
            u_index = i * 4
            v_index = i * 4 + 2 
            U[i // UV_WIDTH, i % UV_WIDTH] = raw_data[u_index]
            V[i // UV_WIDTH, i % UV_WIDTH] = raw_data[v_index]
            
        np.savetxt(os.path.join(FILE_DIRNAME, 'Y.txt'), Y, fmt='%d', delimiter=',')
        np.savetxt(os.path.join(FILE_DIRNAME, 'U.txt'), U, fmt='%d', delimiter=',')
        np.savetxt(os.path.join(FILE_DIRNAME, 'V.txt'), V, fmt='%d', delimiter=',')
        
    else:
        Y = np.loadtxt(os.path.join(FILE_DIRNAME, 'Y.txt'), delimiter=',')
        U = np.loadtxt(os.path.join(FILE_DIRNAME, 'U.txt'), delimiter=',')
        V = np.loadtxt(os.path.join(FILE_DIRNAME, 'V.txt'), delimiter=',')
        
    # Test
    print("Y min:", Y.min(), "Y max:", Y.max())
    print("U min:", U.min(), "U max:", U.max())
    print("V min:", V.min(), "V max:", V.max())
    
    return Y, U, V

def yuv2rgb(Y, U, V):
    rgb_data = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
    
    if not os.path.exists(os.path.join(FILE_DIRNAME, 'rgbdata_3d.npy')):
        for i in tqdm(range(IMAGE_SIZE), desc='Converting uyvy to rgb', ncols=100):
    #    for i in range(IMAGE_SIZE):
    
            """ 
            x_index = (i // 2) % UV_WIDTH
            y_index = (i // 2) // UV_WIDTH 
            """
            x_index = (i % IMAGE_WIDTH) // 2
            y_index = i // (2 * IMAGE_WIDTH)
            
            y = Y[i // Y_WIDTH, i % Y_WIDTH]
            
            u = U[y_index, x_index]
            v = V[y_index, x_index]
            
            """             
            r = np.clip(y + 1.402 * (v - 128), 0, 255)
            g = np.clip(y - 0.344136 * (u - 128) - 0.714136 * (v - 128), 0, 255)
            b = np.clip(y + 1.772 * (u - 128), 0, 255)
            """

            """ # BT.709
            r = 1.164 * y + 1.739 * v - 0.97
            g = 1.164 * y - 0.213 * u - 0.533 * v + 0.301
            b = 1.164 * y + 2.112 * u - 1.129 """

            r = 1.164 * y + 1.739 * (v-128) - 0.97
            g = 1.164 * y - 0.213 * (u-128) - 0.533 * (v-128) + 0.301
            b = 1.164 * y + 2.112 * (u-128) - 1.129

            # BT.709
            rgb_data[i // IMAGE_WIDTH, i % IMAGE_WIDTH] = [r, g, b]
#            rgb_data[i // IMAGE_WIDTH, i % IMAGE_WIDTH] = [y, u, v]
#            rgb_data[i // IMAGE_WIDTH, i % IMAGE_WIDTH] = [y, v, u]
#            rgb_data[i // IMAGE_WIDTH, i % IMAGE_WIDTH] = [u, y, v]
#            rgb_data[i // IMAGE_WIDTH, i % IMAGE_WIDTH] = [u, v, y]      
                 
        np.save(os.path.join(FILE_DIRNAME, 'rgbdata_3d.npy'), rgb_data)
    
    else:
        rgb_data = np.load(os.path.join(FILE_DIRNAME, 'rgbdata_3d.npy'))
    
    print("R channel min:", rgb_data[..., 0].min(), "max:", rgb_data[..., 0].max())
    print("G channel min:", rgb_data[..., 1].min(), "max:", rgb_data[..., 1].max())
    print("B channel min:", rgb_data[..., 2].min(), "max:", rgb_data[..., 2].max())
        
        #rgb_data[i // IMAGE_WIDTH, i % IMAGE_WIDTH] = [y, u, v]
        
    return rgb_data
    
if __name__ == '__main__':
    IMAGE_WIDTH = 1920
    IMAGE_HEIGHT = 1536
    IMAGE_SIZE = IMAGE_WIDTH * IMAGE_HEIGHT
    Y_WIDTH = IMAGE_WIDTH
    Y_HEIGHT = IMAGE_HEIGHT
    Y_SIZE = IMAGE_SIZE
    UV_WIDTH = IMAGE_WIDTH // 2
    UV_HEIGHT = IMAGE_HEIGHT // 2
    UV_SIZE = UV_WIDTH * UV_HEIGHT
    FILE_DIRNAME = os.path.dirname(__file__)
    FILE_PATH = os.path.join(FILE_DIRNAME, 'EM728_RGB彩条.yuv')
    
#    regenerate_flag = input('If regenerate all data?(y/n):').lower()
    regenerate_flag = 'y'
#    regenerate_flag = 'n'
    if regenerate_flag == 'y':
        if os.path.exists(os.path.join(FILE_DIRNAME, 'Y.txt')):
            os.remove(os.path.join(FILE_DIRNAME, 'Y.txt'))
        if os.path.exists(os.path.join(FILE_DIRNAME, 'U.txt')):
            os.remove(os.path.join(FILE_DIRNAME, 'U.txt'))
        if os.path.exists(os.path.join(FILE_DIRNAME, 'V.txt')):
            os.remove(os.path.join(FILE_DIRNAME, 'V.txt'))
        if os.path.exists(os.path.join(FILE_DIRNAME, 'rgbdata_3d.npy')):
            os.remove(os.path.join(FILE_DIRNAME, 'rgbdata_3d.npy'))
            
        print('Files deleted!')

    Y, U, V = read_uyvy(FILE_PATH)
    rgb_data = yuv2rgb(Y, U, V)
    plt.imshow(rgb_data.astype(np.uint8))
    plt.axis('off')
    plt.show()

import numpy as np

def calculate_probability():
    # 获取用户输入的参数
    M = float(input('M='))  # 输入参数M
    S = float(input('S='))  # 输入参数S
    NO = int(input('NO='))  # 输入模拟次数NO
    
    # 生成9行NO列的随机数矩阵，元素范围[0,1)
    R = np.random.rand(9, NO)
    N = 0  # 计数器，记录满足条件的次数
    
    # 计算两个尺度参数a和b
    a = (M * S) ** (1/3)  # 计算x,y方向的缩放系数
    b = (M / S**2) ** (1/3)  # 计算z方向的缩放系数
    
    # 开始NO次模拟
    for k in range(NO):
        # 初始点坐标(x0,y0,z0)，由随机数缩放得到
        x0 = a * R[0, k]
        y0 = a * R[1, k]
        z0 = b * R[2, k]
        
        # 第一个随机方向参数
        phi1 = 2 * np.pi * R[3, k]  # 方位角，[0,2π)
        cthi1 = 2 * R[4, k] - 1  # 极角余弦，[-1,1]
        d1 = R[5, k]  # 第一个位移距离
        
        # 第二个随机方向参数
        phi2 = 2 * np.pi * R[6, k]  # 方位角
        cthi2 = 2 * R[7, k] - 1  # 极角余弦
        d2 = R[8, k]  # 第二个位移距离
        
        # 计算极角正弦
        sthi1 = np.sqrt(1 - cthi1**2)
        sthi2 = np.sqrt(1 - cthi2**2)
        
        # 计算第一个位移后的点坐标(x1,y1,z1)
        x1 = x0 + d1 * sthi1 * np.cos(phi1)
        y1 = y0 + d1 * sthi1 * np.sin(phi1)
        z1 = z0 + d1 * cthi1
        
        # 计算第二个位移后的点坐标(x2,y2,z2)
        x2 = x0 + d2 * sthi2 * np.cos(phi2)
        y2 = y0 + d2 * sthi2 * np.sin(phi2)
        z2 = z0 + d2 * cthi2
        
        # 检查是否有点落在单位立方体内(所有坐标在[0,1]范围内)
        if ((0 <= x1 <= 1 and 0 <= y1 <= 1 and 0 <= z1 <= 1) or 
            (0 <= x2 <= 1 and 0 <= y2 <= 1 and 0 <= z2 <= 1)):
            N += 1  # 满足条件则计数器加1
    
    # 计算并返回概率估计值
    probability = N / NO
    return probability

# 主程序入口
if __name__ == "__main__":
    prob = calculate_probability()
    print(f"概率估计值: {prob:.4f}")  # 输出保留4位小数的概率

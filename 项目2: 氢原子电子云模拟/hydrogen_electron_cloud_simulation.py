import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# 物理常数
a0 = 5.29e-11  # 玻尔半径 (m)
pmax = 1.1      # 概率密度最大值 (归一化单位)
ro = 0.25e-9    # 收敛半径 (m)

def wave_function(r):
    """氢原子基态波函数 (球对称)"""
    return (1.0 / (np.sqrt(np.pi) * a0**1.5)) * np.exp(-r / a0)

def probability_density(r):
    """概率密度函数 |ψ|²"""
    psi = wave_function(r)
    return np.abs(psi)**2

def generate_electron_positions(num_points):
    """生成电子位置样本 (球坐标系)"""
    # 使用接受-拒绝抽样法生成符合概率密度的径向距离
    r_values = []
    max_r = 5 * a0  # 最大采样半径
    
    while len(r_values) < num_points:
        r_candidate = np.random.uniform(0, max_r)
        z_candidate = np.random.uniform(0, pmax)
        
        # 接受符合概率密度的点
        if z_candidate < probability_density(r_candidate):
            r_values.append(r_candidate)
    
    r_values = np.array(r_values)
    
    # 生成随机角度 (球坐标系)
    theta_values = np.arccos(2 * np.random.random(num_points) - 1)  # θ ∈ [0, π]
    phi_values = np.random.uniform(0, 2 * np.pi, num_points)        # φ ∈ [0, 2π]
    
    # 转换为笛卡尔坐标系
    x = r_values * np.sin(theta_values) * np.cos(phi_values)
    y = r_values * np.sin(theta_values) * np.sin(phi_values)
    z = r_values * np.cos(theta_values)
    
    return x, y, z

def plot_electron_cloud(x, y, z):
    """可视化电子云分布"""
    # 3D点云图
    fig = plt.figure(figsize=(15, 10))
    
    # 3D散点图
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.scatter(x, y, z, s=0.1, alpha=0.3, c='b')
    ax1.set_title('3D Electron Cloud')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    
    # XY平面投影
    ax2 = fig.add_subplot(222)
    ax2.scatter(x, y, s=0.1, alpha=0.3, c='b')
    ax2.set_title('XY Plane Projection')
    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Y (m)')
    ax2.grid(True)
    
    # 径向概率密度分布
    r = np.linspace(0, ro, 1000)
    rho = probability_density(r)
    
    ax3 = fig.add_subplot(223)
    ax3.plot(r, rho, 'r-', linewidth=2)
    ax3.axvline(x=a0, color='g', linestyle='--', label=f'Bohr Radius ({a0:.2e} m)')
    ax3.axvline(x=ro, color='purple', linestyle='--', label=f'Convergence Radius ({ro:.2e} m)')
    ax3.set_title('Radial Probability Density')
    ax3.set_xlabel('Radial Distance (m)')
    ax3.set_ylabel('Probability Density')
    ax3.legend()
    ax3.grid(True)
    
    # 概率密度热力图 (2D切片)
    resolution = 100
    x_grid = np.linspace(-ro, ro, resolution)
    y_grid = np.linspace(-ro, ro, resolution)
    X, Y = np.meshgrid(x_grid, y_grid)
    R = np.sqrt(X**2 + Y**2)
    Z = probability_density(R)
    
    ax4 = fig.add_subplot(224)
    im = ax4.pcolormesh(X, Y, Z, cmap=cm.viridis, shading='auto')
    plt.colorbar(im, label='Probability Density')
    ax4.set_title('2D Probability Density Heatmap')
    ax4.set_xlabel('X (m)')
    ax4.set_ylabel('Y (m)')
    ax4.set_aspect('equal')
    
    plt.tight_layout()
    plt.show()

def analyze_parameter_effects():
    """分析不同参数对电子云分布的影响"""
    # 不同主量子数n的影响
    n_values = [1, 2, 3]
    r_max = 5e-9
    
    plt.figure(figsize=(15, 5))
    for i, n in enumerate(n_values):
        # 不同n的波函数近似
        r = np.linspace(0, r_max, 1000)
        rho = (1/(np.pi*(a0*n)**3)) * np.exp(-2*r/(a0*n))
        
        plt.subplot(1, 3, i+1)
        plt.plot(r, rho, label=f'n = {n}')
        plt.title(f'Effect of Quantum Number n (n={n})')
        plt.xlabel('Radial Distance (m)')
        plt.ylabel('Probability Density')
        plt.grid(True)
        plt.legend()
    
    plt.tight_layout()
    plt.show()

# 主程序
if __name__ == "__main__":
    # 生成电子位置
    num_electrons = 50000
    x, y, z = generate_electron_positions(num_electrons)
    
    # 可视化电子云
    plot_electron_cloud(x, y, z)
    
    # 分析参数影响
    analyze_parameter_effects()


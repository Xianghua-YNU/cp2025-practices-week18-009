import numpy as np

# 参数设置
N = 1000000
np.random.seed(42)  # 确保结果可复现

# 生成随机样本
u = np.random.rand(N)      # 均匀随机数 u ~ U(0,1)
x = u**2                   # 变换得到 x ~ p(x) = 1/(2√x)

# 计算被积函数值
f_star = 2 / (np.exp(x) + 1)

# 计算积分估计
I_hat = np.mean(f_star)

# 计算统计误差
f_star_sq = f_star**2
mean_f_star_sq = np.mean(f_star_sq)
var_f_star = mean_f_star_sq - I_hat**2
sigma = np.sqrt(var_f_star) / np.sqrt(N)

# 输出结果
print(f"积分估计值: {I_hat:.8f}")
print(f"统计误差: {sigma:.8f}")

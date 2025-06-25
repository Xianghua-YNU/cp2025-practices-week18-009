import numpy as np

# 设置随机数种子（可选）
np.random.seed(42)

# 参数设置
N = 1000000

# 生成均匀分布随机数 u_i ~ Uniform(0,1)
u = np.random.rand(N)

# 变换得到服从 p(x) 的随机数 x_i = u_i^2
x = u**2

# 计算 f(x_i) = 2 / (exp(x_i) + 1)
f = 2 / (np.exp(x) + 1)

# 计算积分估计
I_hat = np.mean(f)

# 计算方差估计
f_sq = f**2
mean_f_sq = np.mean(f_sq)
var_f = mean_f_sq - I_hat**2

# 计算统计误差
sigma = np.sqrt(var_f / N)

print(f"积分估计值: {I_hat:.6f}")
print(f"统计误差: {sigma:.6f}")

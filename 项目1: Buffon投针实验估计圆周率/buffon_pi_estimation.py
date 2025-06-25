import random
import math
import matplotlib.pyplot as plt

def buffon_needle_simulation(num_trials, needle_length=1, line_spacing=2):
    """
    执行Buffon投针实验
    
    参数:
        num_trials: 实验次数
        needle_length: 针的长度 (l)
        line_spacing: 平行线间距 (d)
    
    返回:
        π的估计值
    """
    crossings = 0
    
    for _ in range(num_trials):
        # 随机生成针的中心位置和角度
        center = random.uniform(0, line_spacing/2)
        angle = random.uniform(0, math.pi/2)
        
        # 计算针是否与线相交
        if center <= (needle_length/2) * math.sin(angle):
            crossings += 1
    
    if crossings == 0:
        return 0  # 避免除以零
    
    probability = crossings / num_trials
    pi_estimate = (2 * needle_length) / (probability * line_spacing)
    
    return pi_estimate

# 实验不同次数下的π估计
trials_list = [100, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
estimates = []
errors = []

for trials in trials_list:
    estimate = buffon_needle_simulation(trials)
    estimates.append(estimate)
    errors.append(abs(estimate - math.pi))
    print(f"实验次数: {trials:8d}, π估计值: {estimate:.6f}, 误差: {errors[-1]:.6f}")

# 绘制误差随实验次数的变化
plt.figure(figsize=(10, 6))
plt.plot(trials_list, errors, 'bo-')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of experiments (logarithmic scale) ')
plt.ylabel('Absolute error (logarithmic scale) ')
plt.title(' Buffon experiment: Variation of error with the number of experiments')
plt.grid(True)
plt.show()

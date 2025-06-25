import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import random
from matplotlib.gridspec import GridSpec

class ChainReactionSimulator:
    def __init__(self, initial_values=None, rate_constants=None, 
                 stochastic_params=None, max_time=10, time_points=100):
        """
        初始化链式反应模拟器
        
        参数:
        - initial_values: 连续模型的初始浓度 [A0, B0, C0]
        - rate_constants: 连续模型的速率常数 [k1, k2, k3]
        - stochastic_params: 随机模拟参数 {
            'initial_neutrons': 1,
            'fission_prob': 0.5,
            'neutrons_per_fission': 2,
            'max_generations': 20
          }
        - max_time: 连续模型的最大模拟时间
        - time_points: 连续模型的时间点数
        """
        # 设置默认参数
        self.initial_values = initial_values or [1.0, 0.0, 0.0]
        self.rate_constants = rate_constants or [0.5, 0.3, 0.2]
        self.stochastic_params = stochastic_params or {
            'initial_neutrons': 1,
            'fission_prob': 0.5,
            'neutrons_per_fission': 2,
            'max_generations': 20,
            'max_neutrons': 1000
        }
        self.max_time = max_time
        self.time_points = time_points
        
    def continuous_model(self):
        """连续动力学模型模拟"""
        t = np.linspace(0, self.max_time, self.time_points)
        sol = odeint(self._chain_reaction_ode, self.initial_values, t, 
                    args=tuple(self.rate_constants))
        return t, sol.T  # 返回时间和各物质浓度
    
    def _chain_reaction_ode(self, y, t, k1, k2, k3):
        """定义链式反应的动力学方程"""
        A, B, C = y
        dAdt = -k1 * A
        dBdt = k1 * A - k2 * B
        dCdt = k2 * B - k3 * C
        return [dAdt, dBdt, dCdt]
    
    def stochastic_model(self):
        """离散随机模型模拟"""
        params = self.stochastic_params
        neutrons = [params['initial_neutrons']]
        generations = [0]
        
        for gen in range(1, params['max_generations'] + 1):
            prev_neutrons = neutrons[-1]
            if prev_neutrons <= 0:
                break
            if prev_neutrons > params['max_neutrons']:
                break
                
            new_neutrons = 0
            # 将中子数转换为整数
            for _ in range(int(round(prev_neutrons))):
                if random.random() < params['fission_prob']:
                    new_neutrons += params['neutrons_per_fission']
            
            neutrons.append(new_neutrons)
            generations.append(gen)
        
        return generations, neutrons
    
    def run_simulations(self):
        """运行两种模拟并显示结果"""
        # 运行连续模型
        t_cont, concentrations = self.continuous_model()
        A_cont, B_cont, C_cont = concentrations
        
        # 运行随机模型
        gen_stoch, neutrons_stoch = self.stochastic_model()
        
        # 创建绘图
        plt.figure(figsize=(14, 10))
        gs = GridSpec(2, 2, figure=plt.gcf())
        
        # 连续模型结果
        ax1 = plt.subplot(gs[0, 0])
        ax1.plot(t_cont, A_cont, label='Species A')
        ax1.plot(t_cont, B_cont, label='Species B')
        ax1.plot(t_cont, C_cont, label='Species C')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Concentration')
        ax1.set_title('Continuous Kinetic Model')
        ax1.legend()
        ax1.grid(True)
        
        # 随机模型结果(线性尺度)
        ax2 = plt.subplot(gs[0, 1])
        ax2.plot(gen_stoch, neutrons_stoch, 'bo-', linewidth=2, markersize=8)
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Neutron Count')
        ax2.set_title('Stochastic Model (Linear Scale)')
        ax2.grid(True)
        
        # 随机模型结果(对数尺度)
        ax3 = plt.subplot(gs[1, :])
        ax3.semilogy(gen_stoch, neutrons_stoch, 'ro-', linewidth=2, markersize=8)
        ax3.set_xlabel('Generation')
        ax3.set_ylabel('Neutron Count (log scale)')
        ax3.set_title('Stochastic Model (Logarithmic Scale)')
        ax3.grid(True, which="both", ls="--")
        
        plt.tight_layout()
        plt.show()
        
        # 打印临界状态分析
        self._print_criticality_analysis()
    
    def _print_criticality_analysis(self):
        """打印临界状态分析"""
        k1, k2, k3 = self.rate_constants
        p = self.stochastic_params['fission_prob']
        v = self.stochastic_params['neutrons_per_fission']
        
        print("\nCriticality Analysis:")
        print(f"Continuous model characteristic times: τ1={1/k1:.2f}, τ2={1/k2:.2f}, τ3={1/k3:.2f}")
        print(f"Stochastic model multiplication factor: k={p*v:.2f}")
        
        if p * v > 1:
            print("--> Supercritical state (chain reaction will grow exponentially)")
        elif abs(p * v - 1) < 1e-6:  # 考虑浮点数精度
            print("--> Critical state (chain reaction will be self-sustaining)")
        else:
            print("--> Subcritical state (chain reaction will die out)")

# 示例使用
if __name__ == "__main__":
    # 自定义参数
    initial_conc = [1.0, 0.0, 0.0]  # A, B, C的初始浓度
    rate_consts = [0.8, 0.4, 0.1]   # k1, k2, k3
    
    stochastic_params = {
        'initial_neutrons': 1,
        'fission_prob': 0.4,          # 每个中子引发裂变的概率
        'neutrons_per_fission': 2.5,   # 每次裂变产生的中子数
        'max_generations': 20,
        'max_neutrons': 1e6
    }
    
    # 创建模拟器并运行
    simulator = ChainReactionSimulator(
        initial_values=initial_conc,
        rate_constants=rate_consts,
        stochastic_params=stochastic_params,
        max_time=15,
        time_points=200
    )
    
    simulator.run_simulations()

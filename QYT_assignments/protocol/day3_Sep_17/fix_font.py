# import matplotlib
# print(matplotlib.matplotlib_fname())

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

current_dir = Path(__file__).parent
# 生成示例数据
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

# 创建图形
plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.title('正弦波测试中文标题')
plt.xlabel('横轴标签')
plt.ylabel('纵轴标签')

# 保存图形
plt.savefig(f'{current_dir}/test_chinese.png')
plt.show()
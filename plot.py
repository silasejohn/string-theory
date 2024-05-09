import matplotlib.pyplot as plt
import numpy as np


prob_size_x_basic = np.array([20, 96, 180, 448, 640, 674, 920, 1296, 1818, 2048, 2506, 3624, 4298, 5048, 5120])
mem_y_basic = np.array([60336, 60384, 60544, 61280, 62912, 65120, 67904, 74096, 79184, 89856, 91408, 100688, 120208, 129216, 111584])
cpu_y_basic = np.array([0.047206878662109375, 0.5061626434326172, 1.86920166015625, 7.362842559814453, 14.41192626953125, 25.394201278686523, 61.187028884887695, 112.4110221862793, 178.4200668334961, 253.62110137939453, 462.9819393157959, 744.1220283508301, 1481.537103652954, 1846.0659980773926, 1047.307014465332])
mem_y_efficient = np.array([60640, 60656, 60656, 60656, 60656, 60656, 60656, 60656, 60672, 60720, 60720, 60768, 45584, 45728, 46016])
cpu_y_efficient = np.array([0.1010894775390625, 1.0330677032470703, 3.8259029388427734, 13.908863067626953, 28.013944625854492, 49.71003532409668, 112.99705505371094, 204.39600944519043, 316.5931701660156, 447.5829601287842, 829.8139572143555, 1263.291835784912, 2546.0691452026367, 3338.0768299102783, 2079.016923904419])

mem_fit_basic = np.polyfit(prob_size_x_basic, mem_y_basic, 1)
trend_line1 = np.poly1d(mem_fit_basic)
mem_trend_y1 = trend_line1(prob_size_x_basic)

mem_fit_efficient = np.polyfit(prob_size_x_basic, mem_y_efficient, 1)
trend_line3 = np.poly1d(mem_fit_efficient)
mem_trend_y2 = trend_line3(prob_size_x_basic)

cpu_fit_basic = np.polyfit(prob_size_x_basic, cpu_y_basic, 2)
trend_line2 = np.poly1d(cpu_fit_basic)
cpu_trend_y1 = trend_line2(prob_size_x_basic)

cpu_fit_efficient = np.polyfit(prob_size_x_basic, cpu_y_efficient, 2)
trend_line4 = np.poly1d(cpu_fit_efficient)
cpu_trend_y2 = trend_line4(prob_size_x_basic)

# plot a graph for cpu_time vs problem_size using cpu_time_array and problem_size_array
plt.plot(prob_size_x_basic, mem_y_basic, color='blue', label='Basic Memory Trend Line')
plt.plot(prob_size_x_basic, mem_y_efficient, color='green', label='Efficient Memory Trend Line')
# plt.plot(prob_size_x_basic, trend_line1(prob_size_x_basic), color='red', label='Basic Memory Trend Line')
# plt.plot(prob_size_x_basic, trend_line3(prob_size_x_basic), color='purple', label='Efficient Memory Trend Line')
plt.xlabel("Problem Size")
plt.ylabel("Memory (KB)")
plt.title("[BASIC] Memory vs Problem Size")
plt.legend()
plt.show()

# plot a graph for cpu_time vs problem_size using cpu_time_array and problem_size_array
plt.plot(prob_size_x_basic, cpu_y_basic, color='blue', label='Basic CPU Time Trend Line')
plt.plot(prob_size_x_basic, cpu_y_efficient, color='green', label='Efficient CPU Time Trend Line')
# plt.plot(prob_size_x_basic, trend_line2(prob_size_x_basic), color='red', label='Basic CPU Time Trend Line')
# plt.plot(prob_size_x_basic, trend_line4(prob_size_x_basic), color='purple', label='Efficient CPU Time Trend Line')
plt.xlabel("Problem Size")
plt.ylabel("CPU Time (ms)")
plt.title("CPU Time vs Problem Size")
plt.legend()
plt.show()
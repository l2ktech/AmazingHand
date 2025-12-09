#!/bin/bash
# AmazingHand 手部追踪启动脚本
# 运行前自动清理占用的进程和串口

echo "=========================================="
echo "AmazingHand 手部追踪启动脚本"
echo "=========================================="

# 1. 杀死所有 dora 进程
echo "[1/5] 停止 dora 进程..."
pkill -9 -f "dora" 2>/dev/null
sleep 1

# 2. 杀死所有 Python 相关进程
echo "[2/5] 停止 Python 节点进程..."
pkill -9 -f "hardware_controller.py" 2>/dev/null
pkill -9 -f "mj_mink_right.py" 2>/dev/null
pkill -9 -f "finger_angle_control.py" 2>/dev/null
pkill -9 -f "main.py" 2>/dev/null
sleep 1

# 3. 释放串口 /dev/ttyACM0
echo "[3/5] 释放串口 /dev/ttyACM0..."
if [ -e /dev/ttyACM0 ]; then
    fuser -k /dev/ttyACM0 2>/dev/null
    sleep 1
    # 确保串口权限正确
    sudo chmod 666 /dev/ttyACM0 2>/dev/null
    echo "  串口已释放"
else
    echo "  [警告] 串口 /dev/ttyACM0 不存在，请检查设备连接"
fi

# 4. 清理僵尸进程
echo "[4/5] 清理僵尸进程..."
sleep 2

# 5. 检查是否还有占用
echo "[5/5] 检查串口状态..."
if fuser /dev/ttyACM0 2>/dev/null; then
    echo "  [警告] 串口仍被占用，尝试强制清理..."
    fuser -k -9 /dev/ttyACM0 2>/dev/null
    sleep 1
else
    echo "  串口空闲，可以使用"
fi

echo ""
echo "=========================================="
echo "清理完成！准备启动手部追踪..."
echo "=========================================="
echo ""
sleep 1

# 6. 设置环境变量并运行
export DISPLAY=:0
cd /home/wzy/AmazingHand/Demo

# 激活 Rust 环境
source ~/.cargo/env

# 运行 dataflow（无超时限制）
echo "启动 dataflow: dataflow_hand_tracking_to_hardware.yml"
echo "按 Ctrl+C 停止程序"
echo ""

dora run dataflow_hand_tracking_to_hardware.yml

# 程序结束后清理
echo ""
echo "=========================================="
echo "程序已停止，清理资源..."
echo "=========================================="

pkill -9 -f "dora" 2>/dev/null
pkill -9 -f "hardware_controller.py" 2>/dev/null
pkill -9 -f "mj_mink_right.py" 2>/dev/null
pkill -9 -f "main.py" 2>/dev/null
fuser -k /dev/ttyACM0 2>/dev/null

echo "清理完成！"

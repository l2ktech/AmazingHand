#!/usr/bin/env python3
"""
AmazingHand 硬件控制节点
接收 Mujoco 仿真输出的关节角度，控制真实硬件
"""

import numpy as np
import pyarrow as pa
from dora import Node
from rustypot import Scs0009PyController
import time


class HardwareController:
    """硬件控制器"""

    def __init__(self, serial_port="/dev/ttyACM0", baudrate=1000000):
        """
        初始化硬件控制器

        Args:
            serial_port: 串口设备路径
            baudrate: 波特率
        """
        print(f"[INFO] 连接到硬件: {serial_port} @ {baudrate}")

        # 初始化舵机控制器
        self.controller = Scs0009PyController(
            serial_port=serial_port,
            baudrate=baudrate,
            timeout=0.5,
        )

        # 启用所有舵机的力矩
        print("[INFO] 启用舵机力矩...")
        for motor_id in range(1, 9):  # ID 1-8
            try:
                self.controller.write_torque_enable(motor_id, 1)
                time.sleep(0.01)
            except Exception as e:
                print(f"[WARN] 舵机 {motor_id} 启用失败: {e}")

        print("[INFO] 硬件控制器初始化完成")

    def write_joint_positions(self, joint_angles):
        """
        写入关节角度到硬件

        Args:
            joint_angles: 8个关节角度（弧度）
        """
        if len(joint_angles) != 8:
            print(f"[ERROR] 期望 8 个关节角度，收到 {len(joint_angles)}")
            return

        # 写入每个舵机
        for motor_id in range(1, 9):
            try:
                angle_rad = joint_angles[motor_id - 1]
                self.controller.write_goal_position(motor_id, angle_rad)
            except Exception as e:
                print(f"[ERROR] 写入舵机 {motor_id} 失败: {e}")

    def set_speed(self, speed=5):
        """设置所有舵机的速度"""
        for motor_id in range(1, 9):
            try:
                self.controller.write_goal_speed(motor_id, speed)
            except Exception as e:
                print(f"[WARN] 设置舵机 {motor_id} 速度失败: {e}")


def main():
    """主函数"""

    # 创建 Dora 节点
    node = Node()

    # 初始化硬件控制器
    try:
        hw = HardwareController(
            serial_port="/dev/ttyACM0",
            baudrate=1000000
        )
        # 设置舵机速度
        hw.set_speed(speed=5)
    except Exception as e:
        print(f"[ERROR] 硬件初始化失败: {e}")
        print("[INFO] 请检查:")
        print("  1. 设备是否连接")
        print("  2. 串口路径是否正确")
        print("  3. 是否有串口权限")
        return

    print("[INFO] 硬件控制节点已启动，等待仿真数据...")

    # 事件循环
    for event in node:
        event_type = event["type"]

        if event_type == "INPUT":
            event_id = event["id"]

            # 接收来自仿真的关节角度
            if event_id == "mj_joints_pos":
                try:
                    # 解析数据
                    joint_angles = event["value"].to_numpy()

                    # 写入硬件
                    hw.write_joint_positions(joint_angles)

                    # 打印调试信息（前10次）
                    if not hasattr(main, 'count'):
                        main.count = 0
                    if main.count < 10:
                        angles_deg = np.rad2deg(joint_angles)
                        print(f"[DEBUG] 第{main.count+1}次: 关节角度 (度): {np.round(angles_deg, 1)}")
                        main.count += 1

                except Exception as e:
                    print(f"[ERROR] 处理关节角度失败: {e}")

            elif event_id == "end":
                print("[INFO] 接收到结束信号")
                break

        elif event_type == "ERROR":
            raise RuntimeError("Dataflow 错误: " + event["error"])

    print("[INFO] 硬件控制节点已停止")


if __name__ == "__main__":
    main()

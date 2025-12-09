# Mujoco 仿真测试结果

测试时间: 2025-12-09

## ✓ 测试成功！

### 测试的程序

#### 1. finger_angle_control.py
- **功能**: 生成周期性的手指角度控制命令
- **状态**: ✓ 正常运行
- **说明**: 使用正弦波生成手指的俯仰(pitch)和滚转(roll)角度

#### 2. mj_mink_right.py
- **功能**: 右手 Mujoco 物理仿真 + 逆运动学求解
- **状态**: ✓ 正常运行并显示
- **说明**: 使用 Mink 库求解逆运动学，将手指末端姿态转换为舵机角度

### 环境配置

#### Python 环境
- **版本**: Python 3.10
- **虚拟环境**: Demo/.venv

#### 已安装的依赖
| 包名 | 用途 | 状态 |
|------|------|------|
| mujoco | 3D 物理仿真引擎 | ✓ |
| mink | 逆运动学求解器 | ✓ |
| qpsolvers | 二次规划求解器 | ✓ |
| quadprog | QP 求解器后端 | ✓ |
| dora-rs | 数据流框架 | ✓ |
| scipy | 科学计算（旋转矩阵） | ✓ 升级到 1.15.3 |
| pyarrow | 数据序列化 | ✓ |
| loop-rate-limiters | 循环速率控制 | ✓ |

### 运行配置

#### Dora 数据流
```yaml
nodes:
  - id: move_angle
    path: AHSimulation/examples/finger_angle_control.py
    inputs:
      tick: dora/timer/millis/50  # 50ms 周期
    outputs:
      - hand_quat

  - id: hand_simulation_r
    path: AHSimulation/AHSimulation/mj_mink_right.py
    inputs:
      r_hand_quat: move_angle/hand_quat
      tick: dora/timer/millis/2   # 2ms 周期
      tick_ctrl: dora/timer/millis/10  # 10ms 控制周期
    outputs:
      - mj_r_joints_pos
    args: -m quat  # 四元数模式（控制方向）
```

#### 显示设置
- **DISPLAY**: :0 (GNOME 桌面)
- **渲染**: OpenGL 硬件加速
- **查看器**: Mujoco 内置被动查看器

### 解决的问题

#### 1. Python 版本兼容性
- **问题**: AHSimulation 需要 Python 3.12，但基础环境是 3.10
- **解决**: 在 Demo 目录创建独立的 Python 3.12 虚拟环境

#### 2. scipy as_quat() 参数
- **问题**: 旧版 scipy 不支持 `scalar_first` 参数
- **解决**: 升级 scipy 到 1.15.3

#### 3. DISPLAY 环境变量
- **问题**: 没有设置 DISPLAY，Mujoco 无法打开窗口
- **解决**: 设置 `export DISPLAY=:0`

#### 4. quadprog 求解器
- **问题**: mink 默认使用 quadprog 求解器，但未安装
- **解决**: `pip install qpsolvers[quadprog]`

#### 5. 可编辑安装问题
- **问题**: `pip install -e AHSimulation` 失败（缺少 setup.py）
- **解决**: 使用普通安装或直接指定 Python 路径

## 运行命令

### 启动 Dora Daemon
```bash
source ~/.cargo/env
dora up
```

### 运行仿真（在 GNOME 桌面显示）
```bash
export DISPLAY=:0
cd /home/wzy/AmazingHand/Demo
source ~/.cargo/env
dora run dataflow_angle_simu_test2.yml
```

### 停止仿真
按 `Ctrl+C` 或关闭 Mujoco 窗口

### 停止 Dora Daemon
```bash
dora destroy
```

## 仿真功能

### 当前演示
- **手指运动**: 所有手指（食指、中指、无名指、大拇指）执行周期性的弯曲和展开动作
- **运动模式**: 正弦波，频率 1Hz
- **控制模式**: 四元数控制（orientation control）

### 可选模式
修改 `args: -m quat` 为 `args: -m pos` 可切换到位置控制模式

## 系统架构

```
finger_angle_control.py (50ms)
    ↓ hand_quat (四元数)
mj_mink_right.py (2ms tick, 10ms ctrl)
    ↓ 逆运动学求解
    ↓ mj_r_joints_pos (舵机角度)
    ↓
[Mujoco 物理引擎] → [OpenGL 渲染] → [GNOME 桌面显示]
```

## 性能

- **渲染帧率**: 实时（根据硬件性能）
- **控制频率**: 500 Hz (2ms tick)
- **命令频率**: 20 Hz (50ms)
- **物理步长**: 默认 (Mujoco 配置)

## 文件位置

- **仿真模型**: `Demo/AHSimulation/AH_Right/mjcf/scene.xml`
- **右手脚本**: `Demo/AHSimulation/AHSimulation/mj_mink_right.py`
- **角度控制**: `Demo/AHSimulation/examples/finger_angle_control.py`
- **数据流配置**: `Demo/dataflow_angle_simu_test2.yml`

## 下一步

### 可以尝试的功能

1. **手部追踪仿真**
   ```bash
   cd /home/wzy/AmazingHand/Demo
   dora build dataflow_tracking_simu.yml
   dora run dataflow_tracking_simu.yml
   ```

2. **真实硬件 + 手部追踪**
   ```bash
   cd /home/wzy/AmazingHand/Demo
   dora build dataflow_tracking_real.yml
   dora run dataflow_tracking_real.yml
   ```
   需要：摄像头 + 连接的 AmazingHand 硬件

3. **双手仿真**
   ```bash
   # 修改数据流添加 hand_simulation_l 节点
   ```

## 总结

✓ **所有测试通过！**

1. ✓ Mujoco 仿真环境成功配置
2. ✓ 手指角度控制程序正常工作
3. ✓ 逆运动学求解正确
4. ✓ 3D 可视化正常显示
5. ✓ Dora 数据流正常运行

您现在拥有一个完整的机械手仿真系统，可以用于：
- 算法测试
- 运动规划验证
- 控制策略开发
- 可视化展示

---
测试人员: Claude Code
测试日期: 2025-12-09

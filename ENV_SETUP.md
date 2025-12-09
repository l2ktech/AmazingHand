# AmazingHand 环境设置说明

## 已安装的组件

### 1. Python 虚拟环境
- **位置**: `/home/wzy/AmazingHand/env`
- **Python 版本**: 3.10.12

### 2. 已安装的 Python 包

| 包名 | 版本 | 用途 |
|------|------|------|
| numpy | 2.2.6 | 数值计算 |
| opencv-python | 4.12.0 | 图像处理 |
| mediapipe | 0.10.14 | 手部追踪 |
| scipy | 1.15.3 | 科学计算 |
| pyarrow | 22.0.0 | 数据序列化 |
| rustypot | 1.4.0 | 舵机控制 |
| dora-rs | 0.3.13 | 机器人数据流框架 |
| loop-rate-limiters | 1.2.0 | 循环速率控制 |

### 3. Rust 工具链
- **Rust 版本**: 1.91.1
- **dora-cli 版本**: 0.3.13
- **安装位置**: `~/.cargo`

## 使用方法

### 激活虚拟环境

```bash
source env/bin/activate
```

### 加载 Rust 环境

```bash
source ~/.cargo/env
```

### 运行基础测试

#### 测试 Python 环境
```bash
env/bin/python test_env.py
```

#### 测试基础示例（需要连接设备）
```bash
# 激活环境
source env/bin/activate

# 运行演示程序
python PythonExample/AmazingHand_Demo.py

# 运行手指测试
python PythonExample/AmazingHand_FingerTest.py

# 运行校准程序
python PythonExample/AmazingHand_Hand_FingerMiddlePos.py
```

### 运行 Dora 仿真示例

#### 1. 启动 dora daemon
```bash
source ~/.cargo/env
dora up
```

#### 2. 构建数据流（首次运行）
```bash
cd Demo
dora build dataflow_angle_simu.yml --uv
```

#### 3. 运行仿真
```bash
dora run dataflow_angle_simu.yml --uv
```

#### 4. 运行手部追踪仿真
```bash
# 构建
dora build dataflow_tracking_simu.yml --uv

# 运行
dora run dataflow_tracking_simu.yml --uv
```

#### 5. 运行手部追踪真实硬件
```bash
# 构建
dora build dataflow_tracking_real.yml --uv

# 运行
dora run dataflow_tracking_real.yml --uv
```

## 串口配置

所有 PythonExample 中的程序已配置为使用 `/dev/ttyACM0`

## 权限设置

如果遇到串口权限问题：

### 临时方案
```bash
sudo chmod 666 /dev/ttyACM0
```

### 永久方案
```bash
# 已添加用户到 dialout 组
# 需要重新登录才能生效
sudo usermod -a -G dialout $USER
```

## 常见问题

### Q: 虚拟环境如何退出？
```bash
deactivate
```

### Q: 如何检查 dora 是否运行？
```bash
dora list
```

### Q: 如何停止 dora daemon？
```bash
dora destroy
```

### Q: 如何重新安装依赖？
```bash
# Python 依赖
env/bin/pip install -r requirements.txt

# Rust dora-cli
cargo install dora-cli
```

## 测试文件

- `test_env.py` - 测试 Python 环境依赖

## 下一步

1. 确认设备连接到 `/dev/ttyACM0`
2. 测试基础示例程序
3. 尝试运行 Dora 仿真
4. 如需手部追踪，确保摄像头正常工作

---
创建时间: 2025-12-09

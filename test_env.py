#!/usr/bin/env python3
"""
测试环境依赖是否正确安装
"""

import sys

def test_imports():
    """测试所有必需的包是否可以导入"""

    packages = {
        'numpy': 'NumPy',
        'cv2': 'OpenCV',
        'mediapipe': 'MediaPipe',
        'scipy': 'SciPy',
        'pyarrow': 'PyArrow',
        'rustypot': 'RustyPot',
    }

    print("测试环境依赖...")
    print("=" * 50)

    all_good = True

    for module, name in packages.items():
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'unknown')
            print(f"✓ {name:15} - 版本 {version}")
        except ImportError as e:
            print(f"✗ {name:15} - 未安装")
            all_good = False

    print("=" * 50)

    if all_good:
        print("\n✓ 所有依赖包都已正确安装!")
        return 0
    else:
        print("\n✗ 部分依赖包未安装")
        return 1

if __name__ == '__main__':
    sys.exit(test_imports())

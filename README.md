## 产品型号解析器（多厂商、多规则）

本项目提供一个可扩展的产品型号解析框架：自动加载 `parsers/` 下的解析规则，按顺序检测并解析不同厂商与系列的型号字符串，支持表格或 JSON 输出，便于终端查看或与系统对接。

### 主要特性
- 动态加载解析规则：新增一个 `parsers/*.py` 文件即可生效
- 自动检测解析器：每个解析器暴露 `detect(model)` 与 `parse(model)` 即可
- 多格式输出：`--format table` 与 `--format json`
- 字段并集展示：表格模式会合并所有解析结果的字段作为列

### 目录结构
```text
product_parse/
├── core.py
└── parsers/
    ├── xyz100.py
    ├── sv630p.py
    ├── motor_ac.py
    ├── plc_ab200.py
    └── sensor_tx.py
```

### 安装与环境
- 依赖：Python 3.10+
- 克隆仓库后，直接运行，无需额外依赖
- macOS/Linux 通常使用 `python3`；Windows 可能使用 `python`

### 快速开始
```bash
cd product_parse
python3 core.py --format table --models SV630PS2R8I XY1A-220-05KW-F AC-M-2KW-1500-90 AB200-IO032 TX-PT-10K-V1
```

### 示例输出（表格）
```text
✅ 已加载解析规则: ['sv630p', 'xyz100', 'motor_ac', 'plc_ab200', 'sensor_tx']
解析结果（表格）:
型号              | 产品组族 | 产品系列 | 产品类型 | 电压等级 | 额定电流 | 安装方式 | 系列   | 类型 | 电压 | 功率  | 功能 | 额定功率 | 额定转速 | 机座号 | I/O点数 | 通信接口 | 测量类型 | 量程 | 版本 | 错误
------------------+--------+--------+--------+--------+--------+--------+------+----+----+-----+----+--------+--------+------+--------+--------+--------+----+----+----
SV630PS2R8I       | Servo | 630    | 脉冲型   | 220V   | 2.8A   | 基板标准 |      |    |    |     |    |        |        |      |        |        |        |    |    |    
XY1A-220-05KW-F   |        |        |         |        |        |        | XYZ100 | 脉冲 | 220 | 05KW | F  |        |        |      |        |        |        |    |    |    
AC-M-2KW-1500-90  |        |        |         |        |        |        |      |    |    |     |    | 2KW    | 1500   | 90   |        |        |        |    |    |    
AB200-IO032       |        |        |         |        |        |        |      |    |    |     |    |        |        |      | 032    | Ethernet |        |    |    |    
TX-PT-10K-V1      |        |        |         |        |        |        |      |    |    |     |    |        |        |      |        |        | PT     | 10K | V1 |    
```

### 示例：驱动器型号和铭牌说明

![SV630P 驱动器铭牌示例](pic/SV630P.png)

> 以上图片用于说明 SV630P 系列的铭牌信息与型号编码位置，便于对照解析字段。

### JSON 模式
```bash
python3 core.py --format json --models SV630PS2R8I XY1A-220-05KW-F
```
输出：
```json
[
  {
    "型号": "SV630PS2R8I",
    "产品组族": "Servo",
    "产品系列": "630",
    "产品类型": "脉冲型",
    "电压等级": "220V",
    "额定电流": "2.8A",
    "安装方式": "基板标准"
  },
  {
    "型号": "XY1A-220-05KW-F",
    "系列": "XYZ100",
    "类型": "脉冲",
    "电压": "220",
    "功率": "05KW",
    "功能": "F"
  }
]
```

### CLI 说明
- `--format`：输出格式，`table` 或 `json`（默认 json）
- `--models`：待解析的型号字符串，空则使用内置示例

### API 用法（代码中调用）
```python
from core import load_parsers, parse_models

load_parsers()
results = parse_models(["SV630PS2R8I", "XY1A-220-05KW-F"])  # list[dict]
```

### 编写新解析器
在 `parsers/` 新增一个文件（例如 `abc900.py`），实现以下两个函数：
```python
def detect(model: str) -> bool:
    return model.startswith("ABC900")

def parse(model: str) -> dict[str, str]:
    # 解析并返回字段字典
    return {"型号": model, "系列": "ABC900"}
```
保存后无需修改 `core.py`，运行时会自动被加载。

### 现有解析器概览
- `sv630p.py`：SV630 伺服驱动器
- `xyz100.py`：XYZ100 变频器，支持 XY1A/XY1B 前缀
- `motor_ac.py`：交流电机 AC-M*
- `plc_ab200.py`：PLC AB200 系列
- `sensor_tx.py`：TX 系列传感器

### 注意与字段对齐
- `sv630p.py` 输出键名为：`产品组族`、`产品系列`、`产品类型`、`电压等级`、`额定电流`、`安装方式`
- 其他解析器可自由返回自身字段；表格模式会合并为列

### 常见问题
- 表格列顺序：由首次出现字段的顺序决定
- 新增解析器不生效：确认文件名以 `.py` 结尾，且未以下划线开头；并实现 `detect`/`parse`
- JSON 中文显示为 Unicode：`core.py` 已设置 `ensure_ascii=False`
- 已加载解析规则的顺序：与文件系统遍历顺序相关，可能与示例略有不同，不影响解析
- 表格宽度：根据内容动态调整，若终端较窄可能自动换行或折叠

### 许可证
MIT

### 贡献
欢迎提交 Issue 和 Pull Request！



### 变更日志
建议遵循语义化版本号（MAJOR.MINOR.PATCH）：
- 破坏性变更：MAJOR +1（例如字段名更改）
- 向下兼容的新功能：MINOR +1（新增解析器或新字段）
- 向下兼容的问题修复：PATCH +1（修正文案或边界解析）

示例（Changelog）
```text
v1.1.0
- feat: 新增解析器 abc900
- feat: `sv630p` 新增电压等级映射 T->380V

v1.0.1
- fix: 修正 `xyz100` 对 XY1B 功能字段的解析

v1.0.0
- init: 初始发布，支持 sv630p/xyz100/motor_ac/plc_ab200/sensor_tx
```

### 发布流程
以 Git Tag 与 GitHub Release 为例：
```bash
# 1) 更新版本与变更日志（编辑 README 或 CHANGELOG.md）

# 2) 提交代码
git add .
git commit -m "docs: update changelog for v1.1.0"

# 3) 打 Tag
git tag v1.1.0

# 4) 推送分支与 Tag
git push origin main --tags

# 5) 在 GitHub 的 Releases 页面创建新版本说明
#   - 标题：v1.1.0
#   - 内容：复制“变更日志”对应版本的内容
```


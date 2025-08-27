# parsers/plc_ab200.py
def detect(model: str) -> bool:
    """匹配 AB200 系列PLC"""
    return model.upper().startswith("AB200")

def parse(model: str) -> dict[str, str]:
    return {
        "型号": model,
        "系列": "PLC AB200",
        "I/O点数": model[-3:],  # 最后三位表示点数
        "通信接口": "Ethernet" if "E" in model else "串口"
    }

# parsers/motor_ac.py
def detect(model: str) -> bool:
    """匹配 AC-M 开头的交流电机型号"""
    return model.startswith("AC-M")

def parse(model: str) -> dict[str, str]:
    parts = model.split("-")
    return {
        "型号": model,
        "系列": "AC电机",
        "额定功率": parts[1] if len(parts) > 1 else "",
        "额定转速": parts[2] if len(parts) > 2 else "",
        "机座号": parts[3] if len(parts) > 3 else ""
    }

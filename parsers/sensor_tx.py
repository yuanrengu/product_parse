# parsers/sensor_tx.py
def detect(model: str) -> bool:
    """匹配 TX 系列传感器"""
    return model.startswith("TX")

def parse(model: str) -> dict[str, str]:
    # 例: TX-PT-10K-V1
    parts = model.split("-")
    return {
        "型号": model,
        "系列": "TX传感器",
        "测量类型": parts[1] if len(parts) > 1 else "",
        "量程": parts[2] if len(parts) > 2 else "",
        "版本": parts[3] if len(parts) > 3 else ""
    }

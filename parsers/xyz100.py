def detect(model: str) -> bool:
    return model.startswith("XY1A") or model.startswith("XY1B")

def parse(model: str) -> dict[str, str]:
    parts = model.split("-")
    type_map = {"A": "脉冲", "B": "总线"}
    return {
        "型号": model,
        "系列": "XYZ100",
        "类型": type_map.get(parts[0][-1], "未知"),
        "电压": parts[1],
        "功率": parts[2],
        "功能": parts[3] if len(parts) > 3 else ""
    }

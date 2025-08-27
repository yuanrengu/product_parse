# 检测规则
def detect(model: str) -> bool:
    return model.startswith("SV630")

# 实际解析规则
def parse(model: str) -> dict[str, str]:
    family_map = {"SV": "Servo"}
    type_map = {"P": "脉冲型", "A": "CANlink", "C": "CANopen"}
    voltage_map = {"S": "220V", "T": "380V"}
    current_map = {
        "1R6": "1.6A", "2R8": "2.8A", "3R5": "3.5A", "5R4": "5.4A",
        "5R5": "5.5A", "7R6": "7.6A", "012": "12A", "017": "16.5A",
        "021": "20.8A", "026": "25.7A",
    }
    install_map = {"I": "基板标准"}

    return {
        "型号": model,
        "产品组族": family_map.get(model[0:2], "未知"),
        "产品系列": model[2:5],
        "产品类型": type_map.get(model[5], "未知"),
        "电压等级": voltage_map.get(model[6], "未知"),
        "额定电流": current_map.get(model[7:-1], "未知"),
        "安装方式": install_map.get(model[-1], "未知")
    }

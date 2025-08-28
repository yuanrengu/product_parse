import os
import importlib
import json

PARSERS = {}
DETECTORS = []
_LOADED = False


def load_parsers():
    """动态加载 parsers/ 目录下所有解析器"""
    global _LOADED
    if _LOADED:
        return
    parser_dir = os.path.join(os.path.dirname(__file__), "parsers")
    for fname in os.listdir(parser_dir):
        if fname.endswith(".py") and not fname.startswith("__"):
            mod_name = f"parsers.{fname[:-3]}"
            mod = importlib.import_module(mod_name)
            if hasattr(mod, "detect") and hasattr(mod, "parse"):
                key = fname[:-3]
                PARSERS[key] = mod.parse
                DETECTORS.append((mod.detect, key))
    _LOADED = True


def auto_detect(model: str):
    """自动检测型号属于哪个解析器"""
    for detect, key in DETECTORS:
        if detect(model):
            return key
    return None


def parse_model(model: str) -> dict:
    """解析单个型号"""
    load_parsers()
    key = auto_detect(model)
    if key and key in PARSERS:
        return PARSERS[key](model)
    return {"型号": model, "错误": "未识别型号规则"}


def parse_models(models: list[str]) -> list[dict]:
    """批量解析型号"""
    return [parse_model(m) for m in models]


def to_json(data: list[dict]) -> str:
    """格式化为 JSON"""
    return json.dumps(data, ensure_ascii=False, indent=2)


def to_table(data: list[dict]) -> str:
    """格式化为表格字符串"""
    if not data:
        return "无解析结果"

    headers = []
    for row in data:
        for k in row.keys():
            if k not in headers:
                headers.append(k)

    col_widths = {
        h: max(len(h), max(len(str(r.get(h, ""))) for r in data)) for h in headers
    }

    header_line = " | ".join(f"{h:<{col_widths[h]}}" for h in headers)
    sep_line = "-+-".join("-" * col_widths[h] for h in headers)

    lines = [header_line, sep_line]
    for row in data:
        lines.append(
            " | ".join(f"{str(row.get(h, '')):<{col_widths[h]}}" for h in headers)
        )

    return "\n".join(lines)

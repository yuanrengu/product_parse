import os
import importlib
import argparse
import json
from typing import Any, List, Dict

PARSERS: dict[Any, Any] = {}
DETECTORS = []  # [(detect_func, key)]


def load_parsers():
    """动态加载parsers目录下的所有解析规则文件"""
    parser_dir = os.path.join(os.path.dirname(__file__), "parsers")
    for fname in os.listdir(parser_dir):
        if fname.endswith(".py") and not fname.startswith("__"):
            mod_name = f"parsers.{fname[:-3]}"
            mod = importlib.import_module(mod_name)

            if hasattr(mod, "detect") and hasattr(mod, "parse"):
                key = fname[:-3]
                PARSERS[key] = mod.parse
                DETECTORS.append((mod.detect, key))
    print(f"✅ 已加载解析规则: {list(PARSERS.keys())}")


def auto_detect(model: str) -> str | None:
    """查找匹配的解析器key"""
    for detect, key in DETECTORS:
        if detect(model):
            return key
    return None


def parse_model(model: str) -> dict[str, str]:
    """解析单个型号"""
    key = auto_detect(model)
    if key and key in PARSERS:
        return PARSERS[key](model)
    else:
        return {"型号": model, "错误": "未识别型号规则"}


def parse_models(models: list[str]) -> list[dict[str, str]]:
    """批量解析"""
    return [parse_model(m) for m in models]


def print_table(data: list[dict[str, str]]) -> None:
    """表格形式打印不同字段的结果"""
    if not data:
        print("没有数据")
        return

    # 所有字段（取并集保证不同厂家字段都能显示）
    headers = []
    for d in data:
        for k in d.keys():
            if k not in headers:
                headers.append(k)

    # 计算各列宽度
    col_widths = {
        h: max(len(h), max(len(str(row.get(h, ""))) for row in data)) for h in headers
    }

    # 表头
    header_line = " | ".join(f"{h:<{col_widths[h]}}" for h in headers)
    sep_line = "-+-".join("-" * col_widths[h] for h in headers)
    print(header_line)
    print(sep_line)

    # 行数据
    for row in data:
        print(" | ".join(f"{str(row.get(h, '')):<{col_widths[h]}}" for h in headers))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="多规则型号解析器")
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="json",
        help="输出格式: table(默认) 或 json",
    )
    parser.add_argument("--models", nargs="+", required=False, help="待解析的型号列表")
    args = parser.parse_args()

    load_parsers()

    # 如果没传型号，用默认测试数据
    if args.models:
        models = args.models
    else:
        models = ["SV630PS2R8I", "SV630AT5R5I", "XY1A-220-05KW-F", "ABC123", "SV630CT026I"]

    results = parse_models(models)

    if args.format == "table":
        print("\n解析结果（表格）:")
        print_table(results)
    else:
        print("\n解析结果（JSON）:")
        print(json.dumps(results, ensure_ascii=False, indent=2))

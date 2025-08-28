import argparse
from parser_core import parse_models, to_table, to_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="多规则型号解析器")
    _ = parser.add_argument("--format", choices=["table", "json"], default="json",
                        help="输出格式: table 或 json(默认)")
    _ = parser.add_argument("--models", nargs="+", required=False,
                        help="待解析的型号列表, 空则使用默认示例")
    args = parser.parse_args()

    if args.models:
        models = args.models
    else:
        models = [
            "SV630PS2R8I",
            "SV630AT5R5I",
            "XY1A-220-05KW-F",
            "AC-M-2KW-1500-90",
            "ABC123"
        ]

    results = parse_models(models)

    if args.format == "table":
        print(to_table(results))
    else:
        print(to_json(results))

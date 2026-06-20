import argparse
import sys

from services import (
    add_yacht,
    record_trip,
    record_maintenance,
    monthly_trips,
    yacht_stats,
)


def main():
    parser = argparse.ArgumentParser(description="私家游艇俱乐部管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    p_add = subparsers.add_parser("add-yacht", help="添加船只")
    p_add.add_argument("yacht_id", help="船只编号")
    p_add.add_argument("name", help="船只名称")
    p_add.add_argument("--type", required=True, help="类型：帆船/机动艇/双体船/游艇")
    p_add.add_argument("--length", required=True, help="船长（米）")
    p_add.add_argument("--status", required=True, help="状态：可用/维修/停用")

    p_trip = subparsers.add_parser("trip", help="记录出海")
    p_trip.add_argument("yacht_id", help="船只编号")
    p_trip.add_argument("--captain", required=True, help="船长")
    p_trip.add_argument("--date", required=True, help="日期 YYYY-MM-DD")
    p_trip.add_argument("--start", required=True, help="开始时间 HH:MM")
    p_trip.add_argument("--end", required=True, help="结束时间 HH:MM")
    p_trip.add_argument("--passengers", required=True, help="乘客数")
    p_trip.add_argument("--destination", required=True, help="目的地")

    p_maint = subparsers.add_parser("maintain", help="记录维护")
    p_maint.add_argument("yacht_id", help="船只编号")
    p_maint.add_argument("--date", required=True, help="日期 YYYY-MM-DD")
    p_maint.add_argument("--type", required=True, help="类型：日常保养/引擎维修/船体修复/证件年检")
    p_maint.add_argument("--cost", required=True, help="费用（分，整数）")

    p_month = subparsers.add_parser("monthly-trips", help="月度出海统计")
    p_month.add_argument("--month", required=True, help="月份 YYYY-MM")

    p_stats = subparsers.add_parser("yacht-stats", help="船只统计")
    p_stats.add_argument("yacht_id", help="船只编号")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "add-yacht":
            print(add_yacht(args.yacht_id, args.name, args.type, args.length, args.status))
        elif args.command == "trip":
            print(record_trip(args.yacht_id, args.captain, args.date, args.start, args.end, args.passengers, args.destination))
        elif args.command == "maintain":
            print(record_maintenance(args.yacht_id, args.date, args.type, args.cost))
        elif args.command == "monthly-trips":
            print(monthly_trips(args.month))
        elif args.command == "yacht-stats":
            print(yacht_stats(args.yacht_id))
    except ValueError as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

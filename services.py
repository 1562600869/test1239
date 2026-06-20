from storage import load_data, save_data


YACHT_TYPES = {"帆船", "机动艇", "双体船", "游艇"}
YACHT_STATUSES = {"可用", "维修", "停用"}
MAINTENANCE_TYPES = {"日常保养", "引擎维修", "船体修复", "证件年检"}


def add_yacht(yacht_id, name, yacht_type, length, status):
    if yacht_type not in YACHT_TYPES:
        raise ValueError(f"船只类型必须是: {', '.join(sorted(YACHT_TYPES))}")
    if status not in YACHT_STATUSES:
        raise ValueError(f"船只状态必须是: {', '.join(sorted(YACHT_STATUSES))}")
    try:
        length = float(length)
        if length <= 0:
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError("船长必须是正数")

    data = load_data()
    if yacht_id in data["yachts"]:
        raise ValueError(f"船只编号 {yacht_id} 已存在")

    data["yachts"][yacht_id] = {
        "id": yacht_id,
        "name": name,
        "type": yacht_type,
        "length": length,
        "status": status,
    }
    save_data(data)
    return f"船只 {yacht_id} ({name}) 已添加"


def record_trip(yacht_id, captain, date, start, end, passengers, destination):
    try:
        passengers = int(passengers)
        if passengers <= 0:
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError("乘客数必须是正整数")

    try:
        from datetime import datetime
        start_dt = datetime.strptime(f"{date} {start}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date} {end}", "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("日期时间格式错误，应为 YYYY-MM-DD 和 HH:MM")

    if end_dt <= start_dt:
        raise ValueError("结束时间必须晚于开始时间")

    data = load_data()
    if yacht_id not in data["yachts"]:
        raise ValueError(f"船只 {yacht_id} 不存在")
    if data["yachts"][yacht_id]["status"] != "可用":
        raise ValueError(f"船只 {yacht_id} 当前状态为 {data['yachts'][yacht_id]['status']}，只有可用状态才能出海")

    trip = {
        "yacht_id": yacht_id,
        "captain": captain,
        "date": date,
        "start": start,
        "end": end,
        "passengers": passengers,
        "destination": destination,
    }
    data["trips"].append(trip)
    save_data(data)
    return f"出海记录已添加：{yacht_id} {date} {start}-{end} 前往{destination}"


def record_maintenance(yacht_id, date, mtype, cost):
    if mtype not in MAINTENANCE_TYPES:
        raise ValueError(f"维护类型必须是: {', '.join(sorted(MAINTENANCE_TYPES))}")
    try:
        cost = int(cost)
        if cost < 0:
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError("维护费用必须是非负整数（分）")

    data = load_data()
    if yacht_id not in data["yachts"]:
        raise ValueError(f"船只 {yacht_id} 不存在")

    yacht = data["yachts"][yacht_id]
    if yacht["status"] == "维修":
        raise ValueError(f"船只 {yacht_id} 当前正在维修中，不能重复维护")

    yacht["status"] = "维修"

    record = {
        "yacht_id": yacht_id,
        "date": date,
        "type": mtype,
        "cost": cost,
    }
    data["maintenance"].append(record)
    save_data(data)
    return f"维护记录已添加：{yacht_id} {date} {mtype} 费用{cost}分"


def monthly_trips(month):
    try:
        from datetime import datetime
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise ValueError("月份格式错误，应为 YYYY-MM")

    data = load_data()
    count = 0
    total_passengers = 0
    for trip in data["trips"]:
        if trip["date"].startswith(month):
            count += 1
            total_passengers += trip["passengers"]
    return f"{month} 出海次数：{count} 次，总乘客量：{total_passengers} 人"


def yacht_stats(yacht_id):
    data = load_data()
    if yacht_id not in data["yachts"]:
        raise ValueError(f"船只 {yacht_id} 不存在")

    trip_count = sum(1 for t in data["trips"] if t["yacht_id"] == yacht_id)
    total_cost = sum(m["cost"] for m in data["maintenance"] if m["yacht_id"] == yacht_id)
    return (
        f"船只 {yacht_id} ({data['yachts'][yacht_id]['name']}):\n"
        f"  累计出海次数：{trip_count} 次\n"
        f"  累计维护费用：{total_cost} 分 ({total_cost / 100:.2f} 元)"
    )

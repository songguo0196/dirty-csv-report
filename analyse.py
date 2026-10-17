from pathlib import Path

本文件 = Path(__file__).parent
文件 = 本文件/"data" / "记账数据.csv"

def 读文件(路径):
    try:
        with open(路径, encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"❌ 找不到文件：{路径}")
        print("   检查：路径对不对？文件名拼写对不对？")
        return []
    except UnicodeDecodeError:
        print("❌ 这个文件不是 UTF-8 编码")
        print("   试试把 encoding 改成 gbk")
        return []

def 读明白(路径):

    行们 = 读文件(路径)

    记录们 = []
    问题们 = []

    for 序号,行 in enumerate(行们,1):
        干净 = 行.strip()
        if 序号 == 1 or 干净 == "":
            continue
        列 = 干净.split(",")

        if len(列) < 3 :
            问题们.append((序号, 干净, "列数不够"))
            continue
        金额文字 = 列[2].replace("元", "")
        try:
            金额 = float(金额文字)
        except ValueError:
            问题们.append((序号, 干净, f"金额看不懂：{金额文字!r}"))
            continue

        记录们.append({"日期": 列[0], "项目": 列[1], "金额": 金额})

    return 记录们, 问题们

记录们,问题们 = 读明白(文件)

print(f"收下{len(记录们)}笔")
print(f"跳过{len(问题们)}行")
for 序号,内容,原因 in 问题们:
    print(f"第{序号}行{内容!r}-{原因}")
总支出 = sum(记录["金额"] for 记录 in 记录们)
print(f"总支出 {总支出}")


def 算账(记录们):
    if not 记录们:
        return 0,None,None

    总支出 = sum(记录["金额"] for 记录 in 记录们)

    平均 = 总支出/len(记录们)

    最贵 = None
    for 记录 in 记录们:
        if 最贵 is None or 记录["金额"] > 最贵["金额"]:
            最贵 = 记录

    return 总支出,平均,最贵
总支出, 平均, 最贵 = 算账(记录们)
print(f"总支出 {总支出}")
print(f"平均每笔 {平均}")
print(f"最贵一笔 {最贵}")


输出文件 = 本文件/"data"/"数据分析报告.txt"

行们 = []
行们.append("记账分析报告\n")
行们.append("=" * 48 + "\n\n")

行们.append(f"数据来源：{文件.name}\n")
行们.append(f"生成依据：收下{len(记录们)}笔，跳过{len(问题们)}行\n\n")

if 问题们:  # ← 有跳过才写这一段
    行们.append("跳过明细：\n")
    for 序号, 内容, 原因 in 问题们:
        行们.append(f" 第 {序号} 行 {内容!r} —— {原因}\n")
    行们.append("\n")

行们.append(f"总支出：{总支出}元\n")

if 最贵 is None:
    行们.append(f"平均每笔：本次没有数据，无法计算\n")
    行们.append(f"最贵一笔：本次没有数据\n")

else:
    行们.append(f"平均每笔：{平均}元\n")
    行们.append(f"最贵一笔：{最贵['项目']} {最贵['金额']}元\n")


with open(输出文件,"w",encoding="utf-8") as f:
    f.write("".join(行们))



"""
电子发票查重工具
================

程序功能：
本工具用于财务人员对电子发票进行查重审核，防止重复报销。

程序用法：
使用扫码枪扫描待报销电子发票二维码，获取发票代码、发票号码等信息，与记录的已报销发票数据进行重复比对。
若有重复，说明该发票已报销过，程序给出提示，防止会计重复报销；
若无重复，则可正常报销，程序记录该发票信息，用于下一张发票报销时继续比对。

注意：
首次运行程序时，需保证与脚本同一文件夹下存在 data.csv 文件，
并且首行为“发票代码,发票号码,开票时间,不含税金额,校验码”

名词解释
发票代码：税务部门分配发票的代码，其与发票号码组合成每张发票的唯一标识。
发票号码：税务部门给予发票的号码，其与发票代码组合成每张发票的唯一标识。
开票时间：电子发票开具的时间，通常为电子发票数据产生时间。
（合计）不含税金额：电子发票开具的不含税总金额，即发票明细的不含税金额的总和。
校验码：根据票面生成的一串由数字字母组成的号码。
参考文献：GB/T 36609-2018 电子发票基础信息规范
"""

import csv

# data.csv 中记录了已报销的发票信息
filename = "data.csv"


def get_qrcode_data():
    """从电子发票二维码获取数据"""

    while True:
        # 电子发票二维码存储了发票代码、发票号码、开票日期、不含税金额、校验码等信息(CSV格式)
        qrcode_str = input("请用扫码枪扫描电子发票二维码，\n或者输入n并回车退出程序...\n")

        if qrcode_str == "n":
            fpdm = fphm = kprq = bhsje = jym = ""
            break

        try:
            qrcode_str_stripped = qrcode_str.strip()  # 去除头尾空格字符串
            qrcode_list = qrcode_str.split(",")  # 以','拆分为列表

            fpdm = qrcode_list[2]  # 第3项为发票代码
            fphm = qrcode_list[3]  # 第4项为发票号码
            kprq = qrcode_list[5][:8]  # 第6项为开票日期(只取前8位的YYMMDD)
            bhsje = qrcode_list[4]  # 第5项为不含税金额
            jym = qrcode_list[6][-6:]  # 第7项为校验码(只取后6位)
        except:
            print("电子发票二维码信息有误，请重新扫描！\n")
        else:
            print("读取二维码信息成功！\n")
            break

    # 判断是否退出程序
    if qrcode_str == "n":
        is_exit = True
        qrcode_write_to_file = ""
    else:
        is_exit = False

        # 去除原始字符串中的无关信息，生成写入CSV文件的字符串
        qrcode_write_to_file = fpdm + "," + fphm + "," + kprq + "," + bhsje + "," + jym

        # 显示发票信息
        print("发票代码：" + fpdm)
        print("发票号码：" + fphm)
        print("开票日期：" + kprq)
        print("不含税金额：" + bhsje)
        print("校验码(后6位)：" + jym + "\n")

    return is_exit, fpdm, fphm, kprq, bhsje, jym, qrcode_write_to_file


"""
判断发票是否重复
标准：当待报销的发票代码和发票号码与已报销的某条记录的发票代码和发票号码都相同时才为重复。
算法：先判断发票代码是否重复，再判断发票号码是否重复。
"""


def get_fphm_list_from_fpdm(fpdm):
    """
    从 data.csv 获取已知的发票代码 fpdm 对应的发票号码列表
    若 data.csv 中找不到 fpdm，则 fphm_list_from_fpdm 返回空列表，即 False
    """

    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        # 获取 fphm 对应的所有的发票代码，此处发票代码一定不存在重复元素，故无需判断重复
        fphm_list_from_fpdm = []
        for row in reader:
            if row[0] == fpdm:
                fphm_list_from_fpdm.append(row[1])  # 注意添加的是发票号码，即第2列

    return fphm_list_from_fpdm


def check_validity():
    """查询发票是否重复，若无重复，则写入 data.csv"""

    is_exit, fpdm, fphm, kprq, bhsje, jym, qrcode_write_to_file = get_qrcode_data()

    # 判断是否退出程序
    if is_exit:
        return 0
    else:
        if fphm in get_fphm_list_from_fpdm(fpdm):
            print("*************注意！！！*************")
            print("该发票已报销！不能重复报销！请检查！")
            print("************************************\n")
        else:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(qrcode_write_to_file + "\n")
                print("-------发票信息正常，已保存！-------\n")
        return 1


def main():
    print("****************************")
    print("*     电子发票查重工具     *")
    print("****************************\n")

    while True:
        # 判断是否退出程序
        if check_validity():

            while True:
                # 判断是否继续执行
                mark = input("是否继续发票查重？(y/n)")
                if mark not in ("y", "n"):
                    print("输入错误！请重新输入！\n")
                else:
                    print("\n", end="")
                    break
            if mark == "y":
                print("------------------------------------\n")
            else:
                break

        else:
            break


if __name__ == '__main__':
    main()

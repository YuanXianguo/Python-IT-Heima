# 存储用户信息的列表
info_list = []


def show_line(char, num):
    """显示分割线"""
    print(char*num)


def menu():
    """显示功能菜单"""

    menu_list = ["欢迎使用【名片管理系统】V1.0", "", "1. 新建名片",
                 "2. 显示全部", "3. 查询名片", "", "0. 退出系统"]
    show_line("*", 50)
    for m in menu_list:
        print(m)
    show_line("*", 50)


def add_card():
    """新建名片"""

    print("功能：新建名片")

    name = input("请输入名字：")
    tel_num = input("请输入电话：")
    qq = input("请输入QQ：")
    mail = input("请输入邮箱：")

    info_dict = {"name": name,
                 "tel_num": tel_num,
                 "qq": qq,
                 "mail": mail}

    info_list.append(info_dict)
    print("成功添加{}的名片".format(name))


def info_center(li):
    """格式化输出名片信息"""

    width = 15
    for i in li:
        print(i.center(width), end='')
    print('')


def show_header():
    """输出表格的表头"""

    head_list = ["姓名", "电话", "QQ", "邮箱"]
    info_center(head_list)
    show_line("-", 70)


def show_cards():
    """显示全部名片"""

    print("功能：显示全部")
    if info_list:
        show_header()
        for info_dict in info_list:
            info_center([info_dict["name"], info_dict["tel_num"],
                         info_dict["qq"], info_dict["mail"]])
        show_line("-", 70)
    else:
        print("没有信息")


def query_card():
    """查询名片"""

    print("功能：查询名片")

    name = input("请输入要查询的姓名：")
    for info_dict in info_list:
        if name == info_dict["name"]:
            # 输出查询到的信息
            show_header()
            info_center([info_dict["name"], info_dict["tel_num"],
                         info_dict["qq"], info_dict["mail"]])
            show_line("-", 70)
            update_card(info_dict, name)
            break
    else:
        print("查询信息不存在")


def update_card(info_dict, name):
    num = eval(input(
        "请输入对名片的操作（1：修改/ 2：删除/ 0：返回上级菜单）："))
    if num == 2:
        info_list.remove(info_dict)
        print("信息删除成功！")
    elif num == 0:
        pass
    elif num == 1:
        info_dict["name"] = input_card_info(info_dict["name"],
                                            "请输入姓名[回车不修改]：")
        info_dict["tel_num"] = input_card_info(info_dict["tel_num"],
                                               "请输入电话[回车不修改]：")
        info_dict["qq"] = input_card_info(info_dict["qq"],
                                          "请输入QQ[回车不修改]：")
        info_dict["mail"] = input_card_info(info_dict["mail"],
                                            "请输入邮箱[回车不修改]：")
        print("{}的名片修改成功".format(name))
    else:
        print("请输入正确的指令！")
        update_card(info_dict, name)


def input_card_info(dict_value, mes):
    """输入名片信息

    :param dict_value: 字典原有内容
    :param mes: 提示信息
    :return: 如果用户输入了内容，就返回输入内容，否则就返回字典原有内容
    """
    input_info = input(mes)
    if input_info:
        return input_info
    else:
        return dict_value


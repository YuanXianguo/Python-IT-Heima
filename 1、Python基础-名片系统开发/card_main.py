import card_tools as ct


def main():
    """程序主函数"""

    while True:
        # TODO(daguo) 显示功能菜单
        ct.menu()
        input_num = eval(input("请选择操作功能："))
        print("您选择的操作是：{}".format(input_num))
        ct.show_line("-", 50)
        if input_num == 1:
            ct.add_card()
        elif input_num == 2:
            ct.show_cards()
        elif input_num == 3:
            ct.query_card()
        elif input_num == 0:
            break
        else:
            print("请输入正确的指令！")

    print("欢迎下次使用！")


if __name__ == '__main__':
    main()

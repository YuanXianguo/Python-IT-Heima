def input_pwd():

    pwd = input("请输入密码：")

    if len(pwd) >= 8:
        return pwd

    # 如果密码长度小于8，抛出异常，可以在Exception传入字符串说明信息
    ex = Exception("密码长度不够")

    raise ex


try:
    print(input_pwd())
except Exception as result:
    print("自定义异常：{}".format(result))



import re


def main():
    email = input("请输入要验证的邮箱：")
    res = re.match(r"^([a-zA-Z0-9_]){4,20}@(163|126|qq)\.com$", email)
    if res:
        print(res.group())
        print(res.group(0))
        print(res.group(1))
        print(res.group(2))


if __name__ == '__main__':
    s = "hello@163.com"
    main()

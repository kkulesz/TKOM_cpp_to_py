def strFun(a):
    print("strFun")
    return "strFunReturn"

def main():
    i = 0
    while i < 10:
        print(i)
        strFun(i)
        i = i + 1
    print(False)


if __name__ == "__main__":
    main()
        
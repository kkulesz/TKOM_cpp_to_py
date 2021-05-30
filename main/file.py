def fun(arg1, arg2):
    i = -10
    while i > 0:
        print(i)
        print("\n", end="")
        i = i - 1
        a = (i - 2) * -3
    return -12

def main():
    fun(1, 2)
    return 0


if __name__ == "__main__":
    main()
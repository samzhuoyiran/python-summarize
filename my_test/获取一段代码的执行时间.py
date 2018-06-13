"""计算函数test的执行时间"""

import time


def set_fun(func):
    def call_fun():
        time_flag = time.time()
        func()
        print(time.time() - time_flag)

    return call_fun


@set_fun
def test():
    print("test")
    time.sleep(1)


test()

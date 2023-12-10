

class AppUtils:
    # 打印对象帮助信息
    @staticmethod
    def prt_helper(variable_name, variable, prt_dir=False):
        print("\n")
        if prt_dir:
            print("%s: %s\n%s\n%s\n" % (variable_name, type(variable), variable, dir(variable)))
        else:
            print("%s: %s\n%s\n" % (variable_name, type(variable), variable))
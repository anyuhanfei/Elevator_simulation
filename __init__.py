'''
电梯模拟--参数室
'''

'''运行方式'''
RUN_MODE = 'manual'  # manual or auto

'''运行间隔时间(自动模式生效)'''
UNIT_TIME = 3

'''楼层'''
MAXIMUM_LAYER = 7
MINIMUM_LAYER = 1

'''乘客生成概率'''
PGP = 2  # 最低为1，数值越大，概率越低

'''电梯最大载重'''
MAXIMUM_LOAD = 200  # None为默认载重

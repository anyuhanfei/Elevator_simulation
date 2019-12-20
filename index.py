'''
电梯模拟--总控室
'''
import time
import random

import __init__
from element import mansion
from element import elevator
from element import passenger

# 大楼初始化
mansion_obj = mansion.mansion(__init__.MAXIMUM_LAYER, __init__.MINIMUM_LAYER)

# 电梯初始化
elevator_obj = elevator.elevator()

# 乘客初始化
passenger_objs = dict()

# 开始运营
while(True):
    if input('是否下一步：(Y/N)') == 'N':
        break
    elevator_obj.move_self(__init__.MINIMUM_LAYER, __init__.MAXIMUM_LAYER)
    # 随机生成乘客
    if random.randint(0, 2) == 1:
        passenger_obj = passenger.passenger(__init__.MAXIMUM_LAYER, __init__.MINIMUM_LAYER)
        passenger_objs.update({str(time.time()): passenger_obj})
        # 按按钮
        layer, orientation = passenger_obj.start_task()
        mansion_obj.add_task(layer, orientation)
        # 电梯检索
        elevator_obj.check_mansion_data(mansion_obj)
    # 电梯移动，检测开门
    pop_passenger_keys = []
    if elevator_obj.check_open_door(__init__.MINIMUM_LAYER, __init__.MAXIMUM_LAYER) is True:
        for key, i in passenger_objs.items():
            if i.status is False:  # 未上电梯
                if i.current_layer == elevator_obj.current_layer:  # 电梯到达当前所在楼层
                    if i.orientation == elevator_obj.move_orientation:  # 方向相同
                        i.in_elevator()  # 乘客上电梯
                        if elevator_obj.check_overload(i) is True:  # 超载检测
                            elevator_obj.add_move_task(i)  # 添加移动任务
                            mansion_obj.over_task(i.current_layer, i.orientation)  # 大楼电梯按钮关闭
                        else:
                            i.elevator_overload()  # 超载
            else:  # 已上电梯
                if i.whether_to_over(elevator_obj) is True:  # 到达目的地
                    # 乘客下电梯
                    elevator_obj.remove_passenger(i)
                    pop_passenger_keys.append(key)
    for key in pop_passenger_keys:
        passenger_objs.pop(key)
    elevator_obj.check_mansion_data(mansion_obj)  # 电梯检索

    # 动态打印
    file_content = ''
    for i in range(__init__.MAXIMUM_LAYER, __init__.MINIMUM_LAYER - 1, -1):
        if i == 0:
            continue
        if i == elevator_obj.current_layer:
            file_content += '   电梯   '
        else:
            file_content += '          '
        file_content += '%s  ' % (i)
        file_content += '%s' % (' ↓ ' if mansion_obj.data[str(i)]['down'] is True else '   ')
        file_content += '%s' % (' ↑ ' if mansion_obj.data[str(i)]['up'] is True else '   ')
        file_content += '   '
        for key, value in passenger_objs.items():
            if value.status is False and value.current_layer == i:
                file_content += ' 人(%s) ' % (value.want_layer)
        file_content += '\n'
    # 电梯参数
    file_content += '\n'
    file_content += '电梯任务: %s\n电梯方向：%s\n所在层：%s\n' % (elevator_obj.move_task, elevator_obj.move_orientation, elevator_obj.current_layer)
    file_content += '电梯乘客: '
    for key, value in passenger_objs.items():
        if value.status is True:
            file_content += ' 人(%s) ' % (value.want_layer)
    file_content += '\n'
    # 乘客参数
    file_content += '\n所有乘客:\n'
    for key, value in passenger_objs.items():
        file_content += '所在层：%s  达到层：%s  方向：%s  ' % (value.current_layer, value.want_layer, value.orientation)
        file_content += '乘坐状态：%s  体重：%s\n' % (value.status, value.weight)
    # 保存到文件
    with open('show.log', 'w+', encoding="utf-8") as f:
        f.write(file_content)

    # time.sleep(__init__.UNIT_TIME)

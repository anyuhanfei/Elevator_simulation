'''
电梯模拟--电梯
'''


class elevator():
    maximum_load = 460  # kg  最大载重
    current_layer = 1  # 当前所在层数，初始化为1(电梯无0层)
    passenger_number = 0  # 乘客数量，初始化为0
    passenger_total_weight = 0  # 乘客总重量，初始化为0
    move_task = {'up': set(), 'down': set()}  # 移动任务，乘客需要到达的层数
    move_orientation = 'up'  # 移动方向

    def __init__(self, maximum_load=None):
        self.maximum_load = self.maximum_load if maximum_load is None else maximum_load

    def check_mansion_data(self, mansion_obj):
        '''检测大楼状态
        若有新增的移动任务，则添加
        '''
        for key, value in mansion_obj.data.items():
            if value['up'] is True:
                self.move_task['up'].add(int(key))
            if value['down'] is True:
                self.move_task['down'].add(int(key))

    def move_self(self, minimum_layer, maximum_layer):
        '''移动自己
        每一时间单位执行一次，移动一层
        '''
        if self.update_orientation() is False:
            return
        # 到达顶层没有停留，改变方向后向下了一格（找不到bug，无奈之举）
        if maximum_layer == self.current_layer and self.move_orientation == 'up':
            return
        if minimum_layer == self.current_layer and self.move_orientation == 'down':
            return

        self.current_layer = self.current_layer + 1 if self.move_orientation == 'up' else self.current_layer - 1
        if self.current_layer == 0:
            self.current_layer = self.current_layer + 1 if self.move_orientation == 'up' else self.current_layer - 1

    def add_move_task(self, passenger_obj):
        '''乘客进入电梯完成后，添加移动任务'''
        self.move_task[passenger_obj.orientation].add(passenger_obj.want_layer)

    def check_overload(self, passenger_obj):
        '''超载检测'''
        if self.passenger_total_weight + passenger_obj.weight > self.maximum_load:
            return False
        else:
            self.passenger_number += 1
            self.passenger_total_weight += passenger_obj.weight
            return True

    def check_open_door(self, minimum_layer, maximum_layer):
        '''检测是否开门(即停止)'''
        try:
            self.move_task[self.move_orientation].remove(self.current_layer)
            # self.update_orientation()
            return True
        except BaseException:
            # 不应该开门
            return False

    def remove_passenger(self, passenger_obj):
        '''乘客到达'''
        self.passenger_number -= 1
        self.passenger_total_weight -= passenger_obj.weight

    def update_orientation(self):
        '''更新方向'''
        temp = False
        if self.move_orientation == 'up':  # 检测向上任务中有没有大于我所在层数的
            for i in (self.move_task['down'] | self.move_task['up']):
                if int(i) > self.current_layer:
                    temp = True
                    break
        elif self.move_orientation == 'down':  # 检测向下任务中有没有小于我所在层数的
            for i in (self.move_task['down'] | self.move_task['up']):
                if int(i) < self.current_layer:
                    temp = True
                    break
        if temp is False:
            self.move_orientation = 'down' if self.move_orientation == 'up' else 'up'
        return temp

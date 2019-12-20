'''
电梯模拟--大楼
'''


class mansion():
    maximum_layer = None  # 最高层数
    minimum_layer = 1  # 最低层数
    data = {}  # 每层电梯情况

    def __init__(self, maximum_layer, minimum_layer=None):
        self.maximum_layer = maximum_layer
        self.minimum_layer = minimum_layer if minimum_layer is not None else self.minimum_layer
        self._init_data()

    def _init_data(self):
        '''初始化电梯具体数据'''
        for i in range(self.minimum_layer, self.maximum_layer + 1):
            if i != 0:
                self.data.update({'%s' % (i): {'up': False, 'down': False}})

    def add_task(self, layer, orientation):
        '''乘客按电梯
        将指定楼层的上状态或下状态设置开
        '''
        if orientation == 'up' or orientation == 'down':
            self.data[str(layer)][orientation] = True
            return True
        else:
            return False

    def over_task(self, layer, orientation):
        '''接到乘客
        将指定楼层的上状态或下状态设置关
        '''
        if orientation == 'up' or orientation == 'down':
            self.data[str(layer)][orientation] = False
            return True
        else:
            return False

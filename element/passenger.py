'''
电梯模拟--乘客
'''
import random


class passenger():
    weight = None  # 体重，40~100之间
    current_layer = None  # 当前所在层数
    want_layer = None  # 想要到达层数
    orientation = None  # 方向
    status = False  # 当前乘坐状态，False为等待中，True为乘坐中

    def __init__(self, max_layer, min_layer, weight=None, current_layer=None, want_layer=None):
        self.weight = self._random_weight() if weight is None else weight
        self.current_layer = self._random_current_layer(min_layer, max_layer) if current_layer is None else current_layer
        self.want_layer = self._random_want_layer(min_layer, max_layer) if want_layer is None else want_layer
        self.orientation = 'up' if self.current_layer < self.want_layer else 'down'

    def start_task(self):
        '''开始任务
        在大楼上按电梯按钮,这里只需要返回大楼对象要操作的楼层和上下方向即可
        '''
        return self.current_layer, 'up' if self.current_layer < self.want_layer else 'down'

    def in_elevator(self):
        '''进入电梯'''
        self.status = True

    def elevator_overload(self):
        '''电梯超载
        重新开始任务
        '''
        self.status = False
        return self.start_task()

    def whether_to_over(self, elevator_obj):
        '''是否达到目的层数'''
        if elevator_obj.current_layer == self.want_layer:
            return True
        else:
            return False

    def _random_weight(self):
        '''随机生成体重
        40~50公斤几率：20%
        50~60公斤几率：35%
        60~70公斤几率：30%
        70~80公斤几率：10%
        80~100公斤几率：5%
        '''
        weight_level = [0, 40, 50, 60, 70, 80, 100]
        weight_level_random = [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 5]
        random.shuffle(weight_level_random)
        return random.randint(weight_level[weight_level_random[0]], weight_level[weight_level_random[0] + 1])

    def _random_current_layer(self, min_layer, max_layer):
        '''随机生成所在楼层
        1楼及其下楼层居多
        '''
        for i in range(min_layer, max_layer + 1):
            if i == 0:
                continue
            if i <= 1:
                if random.randint(0, 1) == 1:
                    return i
        return random.randint(2, max_layer)

    def _random_want_layer(self, min_layer, max_layer):
        '''随机生成要去楼层(不与所在楼层相同)
        根据所在楼层随机要求楼层，
        1层和负层：若有负层，高层居多，负层少
        高层：1层和负层居多，其他层少
        '''
        want_layer = 0
        if self.current_layer <= 1:
            want_layer = random.randint(min_layer, max_layer)
        else:
            if random.randint(0, 1) == 1:
                want_layer = random.randint(2, max_layer)
            else:
                want_layer = random.randint(min_layer, 1)
        if want_layer == 0 or want_layer == self.current_layer:
            want_layer = self._random_want_layer(min_layer, max_layer)
        return want_layer

class Power_Supply_Measure(object):
    '''БП дял формирвоания измеряемого тока'''
    def __init__(self, com_port):
        self.port = com_port

    def set_com_port(self):
        '''устаналиваем порт'''
        pass

    def set_mode(self):
        '''устаналиваем режим'''
        pass

    def get_data(self):
        '''получаем данные'''
        pass

    def set_current(self, current):
        '''включаем или отключаем выход'''
        pass
    def set_state_output(self, enable):
        '''включаем или отключаем выход'''
        pass
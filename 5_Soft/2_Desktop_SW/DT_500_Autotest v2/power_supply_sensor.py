class Power_Supply_Sensor(object):
    '''Питание датчиков'''
    def __init__(self, com_port):
        self.port = com_port

    def set_com_port(self):
        '''устаналиваем порт'''
        pass

    def set_mode(self):
        '''устаналиваем режим'''
        pass

    def set_voltage(self, voltage):
        '''устаналиваем режим'''
        pass

    def get_data(self):
        '''получаем данные'''
        pass

    def get_current(self):
        '''получаем данные'''
        pass

    def set_state_output(self, enable):
        '''включаем или отключаем выход'''
        pass
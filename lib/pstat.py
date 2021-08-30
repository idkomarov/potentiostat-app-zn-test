from potentiostat import Potentiostat


class Pstat(Potentiostat):
    def get_test_duration(self, testname, param=None):
        timeunit = 's'
        self.set_param(testname, param)
        return self.get_test_done_time(testname, timeunit=timeunit)

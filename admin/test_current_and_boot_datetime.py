""" Test Set and Get Current and Boot Datetime """
from datetime import date

from lib.current_and_boot_datetime import Set_Current_DateTime


class test_set_current_datetime():

    @classmethod
    def setUpClass(cls):
        """conecting switch"""
        cls.set_cur_dt = Set_Current_DateTime()
        cls.set_cur_dt.connect_switch()
        # cls.set_cur_dt = Set_Current_DateTime()

    def est_set_and_get_current_date_time(self):
        """ testing set current datetime """
        self.set_cur_dt.set_and_get_current_datetime(
            file_name='test_set_and_get_current_date_time.xml')

    def test_set_and_get_boot_date_time(self):
        """ testing set current datetime """
        self.set_cur_dt.set_and_get_boot_datetime(
            file_name='test_set_and_get_boot_date_time.xml')

    def est_set_invalid_datetime(self):
        """ testing set current datetime """
        datestr = date(2013, 12, 30).strftime('%Y-%m-%d')
        self.set_cur_dt.set_invalid_datetime(
            file_name='test_set_invalid_datetime.xml', curr_time = datestr)

import re

import pandas as pd
from pandas._libs.tslibs.nattype import NaT
from datetime import datetime, date

from scripts.utils import FtpConnection, read_gz_text_file


class PlayerTime:
    def __init__(self):
        pass

    def player_times_grouped(self, date_string):
        return \
            self.__players_time_df_group(
                self.__players_time_df_to_delta_df(
                    self.__players_time_df_to_unique_rows(
                        self.__get_players_time_df_historical(date_string)))).to_json()

    def player_times(self, date_string):
        return \
            self.__players_time_df_to_delta_df(
                self.__players_time_df_to_unique_rows(
                    self.__get_players_time_df_historical(date_string))).to_json()

    def players_time_current(self):
        return \
            self.__players_time_df_to_delta_df(
                self.__players_time_df_to_unique_rows(
                    self.__players_time_current())).to_json()

    def __get_players_time_df_historical(self, date_string):
        """

        :param date_string:
        :return:
        """
        LOGPATHS = [date_string + '-1.log.gz']
        users = []
        start_time = []
        end_time = []
        log_reads = []

        conn = FtpConnection()

        for log_file in LOGPATHS:
            conn.ftp_get_binary_file('logs/' + log_file, 'data/' + log_file)
            log = read_gz_text_file('data/' + log_file)
            for line in log:
                entry = line.split(' ')
                if 'joined the game' in line:
                    users.append(entry[3])
                    start_time.append(re.sub("\[|\]", "", entry[0]))
                    end_time.append(None)
                elif 'left the game' in line:
                    users.append(entry[3])
                    end_time.append(re.sub("\[|\]", "", entry[0]))
                    start_time.append(None)

        # %%

        time_data_structure = {
            'users': users,
            'start_time': start_time,
            'end_time': end_time
        }
        time_df = pd.DataFrame(data=time_data_structure)

        for user in time_df.users.unique():
            index = time_df[time_df['users'] == user].index.tolist()[-1]
            if time_df.iloc[index]['end_time'] is None:
                user_close = {'users': user, 'start_time': None, 'end_time': '23:59:59'}
                time_df = time_df.append(user_close, ignore_index=True)

        time_df['start_time'] = pd.to_datetime(time_df['start_time'], format='%H:%M:%S').dt.time
        time_df['end_time'] = pd.to_datetime(time_df['end_time'], format='%H:%M:%S').dt.time
        return time_df

    def __players_time_df_to_unique_rows(self, time_df):
        """

        :param time_df:
        :return:
        """
        pl = []
        st = []
        et = []

        for index, row in time_df.iterrows():
            if row['start_time'] is not NaT and index < len(time_df.index):
                for i in range(index + 1, len(time_df.index)):
                    if row['users'] == time_df.iloc[i]['users']:
                        pl.append(row['users'])
                        st.append(row['start_time'])
                        et.append(time_df.iloc[i]['end_time'])
                        break

        time_sorted_data_structure = {
            'users': pl,
            'start_time': st,
            'end_time': et,
            'delta': [None] * len(et)
        }
        time_sorted_df = pd.DataFrame(data=time_sorted_data_structure)
        return time_sorted_df

    def __players_time_df_to_delta_df(self, time_sorted_df):
        """

        :param time_sorted_df:
        :return:
        """
        for index, row in time_sorted_df.iterrows():
            row['delta'] = datetime.combine(date.today(), row['end_time']) - datetime.combine(date.today(),
                                                                                              row['start_time'])
        return time_sorted_df

    def __players_time_df_group(self, time_sorted_df):
        return time_sorted_df.groupby(['users']).sum()

    def __players_time_current(self):
        conn = FtpConnection()
        latest_log = conn.ftp_get_text_file('/logs/latest.log')
        users = []
        start_time = []
        end_time = []
        log_reads = []

        conn = FtpConnection()

        for line in latest_log:
            entry = line.split(' ')
            if 'joined the game' in line:
                users.append(entry[3])
                start_time.append(re.sub("\[|\]", "", entry[0]))
                end_time.append(None)
            elif 'left the game' in line:
                users.append(entry[3])
                end_time.append(re.sub("\[|\]", "", entry[0]))
                start_time.append(None)

        # %%

        time_data_structure = {
            'users': users,
            'start_time': start_time,
            'end_time': end_time
        }
        time_df = pd.DataFrame(data=time_data_structure)

        for user in time_df.users.unique():
            index = time_df[time_df['users'] == user].index.tolist()[-1]
            if time_df.iloc[index]['end_time'] is None:
                now = datetime.now()
                user_close = {'users': user, 'start_time': None, 'end_time': now.strftime("%H:%M:%S")}
                time_df = time_df.append(user_close, ignore_index=True)

        time_df['start_time'] = pd.to_datetime(time_df['start_time'], format='%H:%M:%S').dt.time
        time_df['end_time'] = pd.to_datetime(time_df['end_time'], format='%H:%M:%S').dt.time
        return time_df

import os
import re

import pandas as pd
from pandas._libs.tslibs.nattype import NaT
from datetime import datetime, date, time

from scripts.utils import FtpConnection, read_gz_text_file


class PlayerTime:
    # Constructor
    """
    @TODO: Fix current log showing end time as 23:59:59 to show current time or something else
    """
    def __init__(self):
        pass

    # Public methods

    def player_times_grouped(self, date_string, previous):
        return \
            self.__players_time_df_group(
                self.__players_time_df_to_delta_df(
                    self.__players_time_df_to_unique_rows(
                        self.__get_players_time_df_historical(date_string, previous)))).to_json()

    def player_times(self, previous, date_string):
        return \
            self.__players_time_df_to_delta_df(
                self.__players_time_df_to_unique_rows(
                    self.__get_players_time_df_historical(previous, date_string))).to_json()

    def players_time_current(self):
        return \
            self.player_times(0, None)

    def get_player_days(self):
        conn = FtpConnection()
        dates = conn.ftp_get_dir_files('logs/')
        dates_mod = ["-".join(day.split("-", 3)[:3]) for day in dates]  # Split and obtain only the dates
        dates_mod.remove('latest.log')
        return sorted(set(dates_mod))

    # Private methods

    def __get_players_time_df_historical(self, previous, *args, **kwargs):

        users = []
        start_time = []
        end_time = []

        conn = FtpConnection()

        files_list = conn.ftp_get_dir_files('/logs')
        logpaths = []
        available_days = self.get_player_days()

        if previous == 0:  # Get only current date logs
            logpaths = ['latest.log']
        else:  # Get n previous logs
            date_index = available_days.index(args[0]) + 1
            for date_string in available_days[date_index - previous:date_index]:
                logpaths = logpaths + [day for day in files_list if date_string in day]

        for log_file in logpaths:
            if not os.path.isfile('data/logs/' + log_file) or log_file=='latest.log':
                conn.ftp_get_binary_file(log_file, 'data/logs/' + log_file)
            if log_file == 'latest.log':
                with open('data/logs/' + log_file) as f:
                    log = list(f)
                log_file = datetime.now().date().isoformat()
            else:
                log = read_gz_text_file('data/logs/' + log_file)
            for line in log:
                entry = line.split(' ')
                if ('joined the game' in line) or ('logged in' in line):
                    user_name = line[line.find(']', line.find(' ')) + 3: line.find('[', line.find(']', line.find(' ')))]
                    users.append(user_name)
                    start_time.append(
                        datetime.combine(
                            date.fromisoformat(log_file[0:10]),
                            time.fromisoformat(re.sub("\[|\]", "", entry[0])))
                    )
                    end_time.append(None)
                elif 'left the game' in line:
                    user_name = line[line.find(']', line.find(' ')) + 3: line.find(' left')]
                    users.append(user_name)
                    end_time.append(
                        datetime.combine(
                            date.fromisoformat(log_file[0:10]),
                            time.fromisoformat(re.sub("\[|\]", "", entry[0])))
                    )
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
                user_close = \
                    {
                        'users': user,
                        'start_time': None,
                        'end_time': datetime.combine(
                            time_df.iloc[index]['start_time'].date(),
                            time.fromisoformat('23:59:59'))
                    }
                time_df = time_df.append(user_close, ignore_index=True)

        # time_df['start_time'] = pd.to_datetime(time_df['start_time'], format='%H:%M:%S').dt.time
        # time_df['end_time'] = pd.to_datetime(time_df['end_time'], format='%H:%M:%S').dt.time
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
            timedelta_diff = row['end_time'] - row['start_time']
            timedelta_diff_minutes = timedelta_diff.total_seconds()
            time_sorted_df.at[index, 'delta'] = timedelta_diff_minutes
        return time_sorted_df

    def __players_time_df_group(self, time_sorted_df):
        pd.set_option("display.max_rows", None, "display.max_columns", None)
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
        print(time_df)
        return time_df

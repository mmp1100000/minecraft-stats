from scripts.utils import get_uuid_from_user, FtpConnection


class PlayerStats:
    def __init__(self, player_name):
        self.player_name = player_name
        self.uuid = get_uuid_from_user(player_name)

    def get_user_stats_json(self):
        conn = FtpConnection()
        return conn.ftp_get_json('/MCW1/stats/'+self.uuid+'.json')
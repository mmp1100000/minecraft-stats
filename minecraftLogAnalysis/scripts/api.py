from flask import Flask
from flask_restful import Resource, Api

from scripts.player_stats import PlayerStats
from scripts.player_time import PlayerTime
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)


class PlayersTimeHistoricalReq(Resource):
    def get(self, date):
        pt = PlayerTime()
        return pt.player_times(date)


class PlayersTimeHistoricalAvalibleDays(Resource):
    def get(self):
        pt = PlayerTime()
        return pt.get_player_days()


class PlayersTimeHistoricalGroupedReq(Resource):
    def get(self, date):
        pt = PlayerTime()
        return pt.player_times_grouped(date, 1)


class PlayersTimeGetCurrentReq(Resource):
    def get(self):
        pt = PlayerTime()
        return pt.players_time_current()


class PlayerStatsReq(Resource):
    def get(self, player_name):
        ps = PlayerStats(player_name)
        return ps.get_user_stats_json()


api.add_resource(PlayersTimeHistoricalReq, '/api/players/time/<date>')

api.add_resource(PlayersTimeHistoricalGroupedReq, '/api/players/time/grouped/<date>')

api.add_resource(PlayersTimeGetCurrentReq, '/api/players/time/current')

api.add_resource(PlayerStatsReq, '/api/players/stats/<player_name>')

api.add_resource(PlayersTimeHistoricalAvalibleDays, '/api/players/days')

if __name__ == '__main__':
    app.run(debug=True)

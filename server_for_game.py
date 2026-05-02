import redis
from flask import Flask, request, jsonify
from flask_cors import CORS
from control_data_base import Problem, db, User
import json
from datetime import datetime

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

app = Flask(__name__)
CORS(app)
app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///mydatabase.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db.init_app(app)


class ControlGame:
    def __init__(self, redis):
        self.matches = "matchmaking:matches"
        self.active = "matchmaking:actives"
        self.r = redis

    def add_user(self, username, elo, subject):
        player_data = {
            "nickname": username,
            "elo": elo,
            "subject": subject
        }

        self.r.zadd(f"matchmaking:queue:{subject}", {json.dumps(player_data): elo})
        response = self.find_match(subject)
        return response

    def find_match(self, subject):
        try:
            players = self.r.zrange(f"matchmaking:queue:{subject}", 0, -1, withscores=True)
            print(f"Очередь до подбора: {players}")
            for i in range(len(players) // 2):
                player1_json = players[i * 2][0]
                player2_json = players[i * 2 + 1][0]
                player1 = json.loads(player1_json)
                player2 = json.loads(player2_json)
                current_time = datetime.now().isoformat()
                match_id = f"match:{current_time}:{player1['nickname']}:{player2['nickname']}"
                task = Problem.get_random_problem(subject)
                match_data = {
                    "username1": player1['nickname'],
                    "username2": player2['nickname'],
                    "elo1": player1["elo"],
                    "elo2": player2["elo"],
                    "task": task[0],
                    "task_id": str(task[1]),
                    "time": current_time,
                    "status": "active",
                    "right_answer": "0",
                    "wrong_answer": "0"
                }

                self.r.hset(f"match:{match_id}", mapping=match_data)
                self.r.sadd("active_matches", match_id)
                self.r.set(f"player:game:{player1['nickname']}", match_id)
                self.r.set(f"player:game:{player2['nickname']}", match_id)
                self.r.zrem(f"matchmaking:queue:{subject}", player1_json)
                self.r.zrem(f"matchmaking:queue:{subject}", player2_json)

            players = self.r.zrange(f"matchmaking:queue:{subject}", 0, -1, withscores=True)
            print(f"Очередь после подбора: {players}")


            return {"status": "success", "message": "user add in queue"}
        except Exception as e:
            print(f"Error: {e}")
            return {"status": "error", "message": str(e)}

    def check_user_match(self, username, elo):
        try:
            match_info = self.r.get(f"player:game:{username}")
            matches = self.r.smembers("active_matches")
            print(matches)
            if match_info and match_info in matches:
                match_data = self.r.hgetall(f"match:{match_info}")
                match_data = {
                    "status": "found",
                    "opponent": match_data["username2"] if match_data["username1"] == username else match_data[
                        "username1"],
                    "your_elo": elo,
                    "opponent_elo": match_data["elo2"] if match_data["elo1"] == elo else match_data[
                        "elo1"],
                    "match": match_data["task"],
                    "time": int((datetime.now() - datetime.fromisoformat(match_data["time"])).total_seconds())
                }
                return match_data
            else:
                player_data1 = json.dumps({
                    "nickname": username,
                    "elo": elo,
                    "subject": "math"
                })
                player_data2 = json.dumps({
                    "nickname": username,
                    "elo": elo,
                    "subject": "physics"
                })

                # Получаем только значения (первый элемент каждого кортежа)
                players1_values = [item[0] for item in self.r.zrange(f"matchmaking:queue:math", 0, -1, withscores=True)]
                players2_values = [item[0] for item in
                                   self.r.zrange(f"matchmaking:queue:physics", 0, -1, withscores=True)]

                if player_data1 in players1_values:
                    return {
                        "status": "waiting",
                        "subject": "math"
                    }
                elif player_data2 in players2_values:
                    return {
                        "status": "waiting",
                        "subject": "physics"
                    }
                else:
                    return {
                        "status": "other"
                    }

        except Exception as e:
            return str(e)

    def cansel_selection(self, username, elo, subject):
        try:
            answer = self.check_user_match(username, elo)
            if answer.get("status") == "waiting":
                print("отмена матча")
                player_data = {
                    "nickname": username,
                    "elo": elo,
                    "subject": subject
                }
                self.r.zrem(f"matchmaking:queue:{subject}", json.dumps(player_data))
                return {
                    "status": "success",
                    "message": "user delete from queue"
                }
            return {
                "status": "error",
                "message": "user already exists in match"
            }
        except Exception as e:
            return str(e)

    def check_answer(self, username, answer):
        try:
            match_info = self.r.get(f"player:game:{username}")
            if match_info:
                match_data = self.r.hgetall(f"match:{match_info}")
                response = Problem.check_right_answer(int(match_data['task_id']), answer)
                response = self.match_results(response, username)
                return response
            return {
                "status": "error",
                "message": "task is not found"
            }
        except Exception as e:
            return str(e)

    def match_results(self, response, username):
        try:
            match_info = self.r.get(f"player:game:{username}")
            if match_info:
                match_data = self.r.hgetall(f"match:{match_info}")
                if response["status"] == "success" and not int(match_data["right_answer"]):
                    User.add_rating(username, 30)
                    User.add_match(username, True)
                    self.r.hset(f"match:{match_info}", "right_answer", "1")
                    self.r.delete(f"player:game:{username}")
                    if int(match_data["wrong_answer"]):
                        self.r.srem("active_matches", match_info)
                    return {
                        "status": "win",
                        "info": "Вы первые дали верный ответ и победили!"
                    }

                elif response["status"] == "success" and int(match_data["right_answer"]):
                    User.add_rating(username, -10)
                    User.add_match(username, False)
                    self.r.delete(f"player:game:{username}")
                    self.r.srem("active_matches", match_info)
                    return {
                        "status": "fail",
                        "info": "Вы дали правильный ответ, но ваш противник оказался сильнее("
                    }

                elif response["status"] == "error" and not int(match_data["wrong_answer"]):
                    self.r.hset(f"match:{match_info}", "wrong_answer", "1")
                    User.add_rating(username, -30)
                    User.add_match(username, False)
                    self.r.delete(f"player:game:{username}")
                    if int(match_data["right_answer"]):
                        self.r.srem("active_matches", match_info)
                    return {
                        "status": "wrong answer",
                        "info": "Вы не смогли дать правильный ответ"
                    }

                elif response["status"] == "error" and int(match_data["wrong_answer"]):
                    User.add_rating(username, -30)
                    User.add_match(username, False)
                    self.r.delete(f"player:game:{username}")
                    self.r.srem("active_matches", match_info)
                    return {
                        "status": "wrong answer",
                        "info": "Вы не смогли дать правильный ответ"
                    }


        except Exception as e:
            return str(e)




@app.route("/api/pvp/add_user", methods=["POST"])
def add_user():
    data = request.json
    username, elo, subject = data.get("username"), data.get("elo"), data.get("subject")
    print(elo)
    response = control_game.add_user(username, elo, subject)
    return response


@app.route("/api/pvp/check_user", methods=["POST"])
def check_user():
    data = request.json
    username, elo = data.get("username"), data.get("elo")
    response = control_game.check_user_match(username, elo)
    return response

@app.route("/api/pvp/cancel_selection", methods=["POST"])
def cansel_selection():
    data = request.json
    username, elo, subject = data.get("username"), data.get("elo"), data.get("subject")
    response = control_game.cansel_selection(username, elo, subject)
    return response

@app.route("/api/pvp/check_answer", methods=["POST"])
def check_answer():
    data = request.json
    user, answer = data.get("user_id"), data.get("his_answer")
    response = control_game.check_answer(user, answer)
    return response

if __name__ == "__main__":
    control_game = ControlGame(r)
    app.run(host="0.0.0.0", port=8001)

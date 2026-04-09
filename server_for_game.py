"""
что бы поднять микросервис, следует установить docker по ссылке https://www.docker.com/products/docker-desktop/
после чего запустить приложение, предварительно в нем зарегистрировавшись
после чего приложение можно закрыть, установить redis, сервер запущен
"""

import redis
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from control_data_base import Problem, db


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


# функция для запрос-ответ логики вывода статуса юзера в игре
def add_user_in_queue(user: str, elo: int, object: str):
    # проверка на наличие созданного матча
    response = r.get(f"pvp:queue:{user}")
    if response:
        match_info = json.loads(response)
        return {
            "status": "found",
            "opponent": match_info["with_whom"],
            "match": match_info["task"]
        }
    # проверка на наличие юзера в очереди на игру
    if r.zscore("pvp:queue", user) is None:
        r.zadd("pvp:queue", {user: elo})

    # создание пар для игры
    queue = r.zrevrange("pvp:queue", 0, -1, withscores=True)
    for i in range(len(queue) // 2):
        user_1, user_2 = queue[i * 2][0], queue[i * 2 + 1][0]
        problem = Problem.get_random_problem(object)
        print(problem)
        match_1 = {
            "with_whom": user_2,
            "task": problem
        }
        match_2 = {
            "with_whom": user_1,
            "task": problem
        }
        r.setex(f"pvp:queue:{user_1}", 5, json.dumps(match_1))
        r.setex(f"pvp:queue:{user_2}", 5, json.dumps(match_2))
        r.zrem("pvp:queue", user_1)
        r.zrem("pvp:queue", user_2)

    # если после создания пара не нашлась: status: waiting
    if r.zscore("pvp:queue", user) is not None:
        return {"status": "waiting"}
    else:
        # если пара есть, создаем игру
        response = r.get(f"pvp:queue:{user}")
        if response:
            match_info = json.loads(response)
            return {
                "status": "found",
                "opponent": match_info["with_whom"],
                "match": match_info["task"]
            }
        # костыль, не нужен, но на всякий
        else:
            return {"status": "waiting"}


# функция для приема запроса на игру
@app.route('/api/pvp/find', methods=['POST'])
def find_match():
    data = request.json
    user = data.get('user_id')
    elo = data.get('rating', 1000)
    print(f"Юзер: {user}")
    object = data.get("object")

    # ошибка запроса
    if not user:
        return jsonify(
            {
            "status": "error",
                        "message": "request_error"
            }
        ), 400

    result = add_user_in_queue(user, elo, object)
    return result
    print(result)

    all_players = r.zrange("pvp:queue", 0, -1, withscores=True)
    print(f"Игроки в очереди {all_players}")
    return jsonify(result)


# функция отмены игры
@app.route('/api/pvp/cancel', methods=['POST'])
def cancel_search():
    data = request.json
    user = data.get('user_id')

    # если матч не начался, отменить игру можно
    if r.zscore("pvp:queue", user) is not None:
        r.zrem("pvp:queue", user)
        r.delete(f"pvp:queue:{user}")
        return jsonify(
            {
                "status": "cancelled",
                "message": "Поиск отменен"
            }
        )

    # если матч начался, ошибка
    match_key = r.get(f"pvp:queue:{user}")
    if match_key:
        return jsonify({"status": "error", "message": "Вы уже в матче"}), 400

    # костыль, но пусть будет
    return jsonify({"status": "not_found", "message": "Вас нет в очереди"})

app.run(host="0.0.0.0", port=8001)
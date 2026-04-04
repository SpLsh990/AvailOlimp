"""
что бы поднять микросервис, следует установить docker по ссылке https://www.docker.com/products/docker-desktop/
после чего запустить приложение, предварительно в нем зарегистрировавшись
после чего приложение можно закрыть, установить redis, сервер запущен
"""

import redis

def add_user_in_queue(user, elo):
    r.zadd("pvp:queue", {user: elo})

def create_battle():
    queue = r.zrevrange("pvp:queue", 0, -1, withscores=True)
    for i in range(len(queue) // 2):
        user1, user2 = queue[i * 2], queue[i * 2 + 1]
        r.rpush("pvp:users", f"{user1[0]},{user2[0]}")
        r.zrem("pvp:queue", user1[0])
        r.zrem("pvp:queue", user2[0])
    

if __name__ == "__main__":
    r = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    )
    queue = r.zrevrange("pvp:queue", 0, -1, withscores=True)
    print(f"Очередь на битву {queue}")
    create_battle()
    pvp_queue = r.lrange("pvp:users", 0, -1)
    print(f"Пары для pvp: {pvp_queue}")
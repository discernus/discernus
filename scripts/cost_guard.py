#!/usr/bin/env python3
"""
Cost Guard Monitor - periodically enforces budget cap for a run
"""
import sys
import time
import redis

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
LUA_SCRIPT_PATH = 'scripts/cost_guard.lua'


def load_lua_script(r):
    with open(LUA_SCRIPT_PATH, 'r') as f:
        script = f.read()
    return r.script_load(script)


def main():
    if len(sys.argv) != 3:
        print("Usage: cost_guard.py <run_id> <budget_cap>")
        sys.exit(1)

    run_id = sys.argv[1]
    try:
        cap = float(sys.argv[2])
    except ValueError:
        print("Invalid budget cap")
        sys.exit(1)

    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    spent_key = f"run:{run_id}:spent"
    # Ensure spent key exists
    if not r.exists(spent_key):
        r.set(spent_key, 0)

    sha = load_lua_script(r)
    print(f"Cost guard loaded, monitoring run {run_id} with cap ${cap}")

    try:
        while True:
            result = r.evalsha(sha, 1, spent_key, cap)
            if result == 0:
                print(f"Budget exceeded for run {run_id}, aborting (status set to ABORTED)")
                break
            time.sleep(5)
    except KeyboardInterrupt:
        print("Cost guard monitor stopped by user")


if __name__ == '__main__':
    main() 
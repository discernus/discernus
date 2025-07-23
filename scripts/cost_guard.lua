-- cost_guard.lua
-- KEYS: [1] = spent_key (e.g., 'run:<RUN_ID>:spent')
-- ARGV: [1] = cap (numeric budget cap)
-- Returns: 1 if under cap; 0 and sets status to 'ABORTED' if over cap

local spent = tonumber(redis.call('GET', KEYS[1]) or '0')
local cap = tonumber(ARGV[1])
if spent > cap then
  -- Abort run by setting status
  local run_id = string.match(KEYS[1], 'run:(.-):spent')
  redis.call('SET', 'run:' .. run_id .. ':status', 'ABORTED')
  return 0
else
  return 1
end 
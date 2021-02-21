INSERT INTO talk_target_tb (
    guild_id,
    vc_id,
    channel_id,
    update_date
)
VALUES (
    %(guild_id)s,
    %(vc_id)s,
    %(channel_id)s,
    to_char(now(), 'YYYYMMDDHH24MISS')
)
ON CONFLICT (guild_id)
DO UPDATE SET
    vc_id = %(vc_id)s,
    channel_id = %(channel_id)s,
    update_date = to_char(now(), 'YYYYMMDDHH24MISS')
;
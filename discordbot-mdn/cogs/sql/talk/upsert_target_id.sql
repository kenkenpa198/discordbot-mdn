INSERT INTO talk_channels (
    guild_id,
    vc_id,
    channel_id,
    updated_at
)
VALUES (
    %(guild_id)s,
    %(vc_id)s,
    %(channel_id)s,
    now()
)
ON CONFLICT (guild_id)
DO UPDATE SET
    vc_id = %(vc_id)s,
    channel_id = %(channel_id)s,
    updated_at = now()
;
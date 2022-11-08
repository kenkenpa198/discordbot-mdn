INSERT INTO played_fortune_users (
    user_id,
    updated_at
)
VALUES (
    %(user_id)s,
    now()
)
;
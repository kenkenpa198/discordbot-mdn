INSERT INTO uranai_played_tb (
    user_id,
    update_date
)
VALUES (
    %(user_id)s,
    now()
)
;
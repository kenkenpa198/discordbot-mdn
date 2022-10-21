INSERT INTO PlayedFortuneUsers (
    user_id,
    updated_at
)
VALUES (
    %(user_id)s,
    now()
)
;
CREATE TABLE IF NOT EXISTS public.calendar
(
    id bigint NOT NULL DEFAULT nextval('calendar_id_seq'::regclass),
    title character varying COLLATE pg_catalog."default",
    comment character varying COLLATE pg_catalog."default",
    start_time bigint,
    end_time bigint,
    is_repeat boolean,
    repeat_until bigint,
    CONSTRAINT calendar_pkey PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS public.calendar_user_association
(
    calendar_id bigint,
    user_id bigint,
    CONSTRAINT calendar_user_association_calendar_id_fkey FOREIGN KEY (calendar_id)
        REFERENCES public.calendar (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT calendar_user_association_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

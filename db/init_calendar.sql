CREATE TABLE IF NOT EXISTS public.calendar
(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    title character varying COLLATE pg_catalog."default",
    comment character varying COLLATE pg_catalog."default",
    start_time bigint,
    end_time bigint,
    is_repeat boolean,
    repeat_until bigint,
    is_delete bool,
    deleted_by bigint,
    CONSTRAINT calendar_users_id_fkey FOREIGN KEY (deleted_by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);

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
);

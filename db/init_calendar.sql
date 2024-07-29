CREATE TABLE IF NOT EXISTS public.calendar
(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    title character varying COLLATE pg_catalog."default",
    comment character varying COLLATE pg_catalog."default",
    start_time bigint,
    end_time bigint,
    is_repeat boolean,
    repeat_until bigint,
    is_delete BOOLEAN DEFAULT FALSE,
    deleted_by bigint,
    CONSTRAINT calendar_users_id_fkey FOREIGN KEY (deleted_by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);

CREATE TYPE user_association_role as ENUM ('creator', 'editor', 'participant');

CREATE TABLE IF NOT EXISTS public.calendar_user_association
(
    id BIGSERIAL PRIMARY KEY,
    calendar_id bigint,
    user_id bigint,
    role user_association_role NOT NULL,
    CONSTRAINT calendar_user_association_calendar_id_fkey FOREIGN KEY (calendar_id)
        REFERENCES public.calendar (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT calendar_user_association_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

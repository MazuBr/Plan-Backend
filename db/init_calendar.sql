CREATE TYPE event_status as ENUM ('active', 'cancel', 'pending');

CREATE TABLE IF NOT EXISTS public.calendar
(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    title character varying COLLATE pg_catalog."default",
    comment character varying COLLATE pg_catalog."default",
    start_time bigint,
    end_time bigint,
    is_delete BOOLEAN DEFAULT FALSE,
    repeat_data JSONB,
    deleted_by bigint,
    parent_id bigint,
    CONSTRAINT calendar_users_id_fkey FOREIGN KEY (deleted_by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT calendar_parent_id_fkey FOREIGN KEY (parent_id)
        REFERENCES public.calendar (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TYPE user_association_role as ENUM ('creator', 'editor', 'participant');

CREATE TABLE IF NOT EXISTS public.calendar_user_association
(
    id BIGSERIAL PRIMARY KEY,
    calendar_id bigint,
    user_id bigint,
    role user_association_role NOT NULL DEFAULT 'participant',
    status event_status NOT NULL,
    CONSTRAINT calendar_user_association_calendar_id_fkey FOREIGN KEY (calendar_id)
        REFERENCES public.calendar (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT calendar_user_association_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT unique_user_calendar UNIQUE (user_id, calendar_id)
);

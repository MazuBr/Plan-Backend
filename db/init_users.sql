CREATE TABLE roles (
    id SMALLSERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO roles (name) VALUES ('admin'), ('user'), ('demo');

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    role SMALLINT REFERENCES roles(id),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    created_at BIGINT DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP),
    updated_at BIGINT DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP),
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at BIGINT
);

CREATE OR REPLACE FUNCTION set_default_role()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.role IS NULL THEN
        NEW.role := (SELECT id FROM roles WHERE name = 'user');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_default_role_trigger
BEFORE INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION set_default_role();
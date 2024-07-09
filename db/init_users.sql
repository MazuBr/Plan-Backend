CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    "role" smallint DEFAULT (
        SELECT id FROM roles WHERE name = 'user'
    ),
    email VARCHAR(100) UNIQUE NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    "address" TEXT,
    created_at BIGINT DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP),
    updated_at BIGINT DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP),
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at BIGINT
);

CREATE TABLE roles (
    id SMALLSERIAL PRIMARY KEY,
    name user_roles UNIQUE NOT NULL
)

INSERT INTO roles (role_name) VALUES ('admin'), ('user'), ('demo');

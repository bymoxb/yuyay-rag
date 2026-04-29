
\connect rag_app;

-- Tablas para una base de datos postgreSQL

CREATE TABLE model(
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name varchar(256) NOT NULL UNIQUE,
    is_default boolean DEFAULT false,
    --
    created_at timestamp DEFAULT now() NOT NULL,
    updated_at timestamp,
    deleted_at timestamp,
    --
    CONSTRAINT model_pk PRIMARY KEY (id)
);

CREATE TABLE department(
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    code varchar(32) NOT NULL UNIQUE,
    name varchar(256) NOT NULL,
    --
    created_at timestamp DEFAULT now() NOT NULL,
    updated_at timestamp,
    deleted_at timestamp,
    --
    CONSTRAINT department_pk PRIMARY KEY (id)
);

CREATE TABLE "user"(
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    full_name varchar(256) NOT NULL,
    email varchar(256) NOT NULL UNIQUE,
    -- department_id uuid,
    --
    created_at timestamp DEFAULT now() NOT NULL,
    updated_at timestamp,
    deleted_at timestamp,
    --
    CONSTRAINT user_pk PRIMARY KEY (id)
    -- ,CONSTRAINT user_department_fk FOREIGN KEY (department_id) REFERENCES department(id)

);

CREATE TABLE chat(
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    title text NOT NULL,
    user_id uuid NOT NULL,
    department_id uuid,
    model_id uuid,
    --
    created_at timestamp DEFAULT now() NOT NULL,
    updated_at timestamp,
    deleted_at timestamp,
    --
    CONSTRAINT chat_pk PRIMARY KEY (id),
    CONSTRAINT chat_user_fk FOREIGN KEY (user_id) REFERENCES "user"(id),
    CONSTRAINT chat_department_fk FOREIGN KEY (department_id) REFERENCES department(id),
    CONSTRAINT chat_model_fk FOREIGN KEY (model_id) REFERENCES model(id)
);

CREATE TABLE message(
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    chat_id uuid NOT NULL,
    user_id uuid,
    content text NOT NULL,
    "role" varchar(50) NOT NULL, -- user, assistant, system
    --
    created_at timestamp DEFAULT now() NOT NULL,
    updated_at timestamp,
    deleted_at timestamp,
    --
    CONSTRAINT message_pk PRIMARY KEY (id),
    CONSTRAINT message_chat_fk FOREIGN KEY (chat_id) REFERENCES chat(id),
    CONSTRAINT message_user_fk FOREIGN KEY (user_id) REFERENCES "user"(id)
);

-- CREATE TABLE role(
--     id uuid DEFAULT gen_random_uuid() NOT NULL,
--     name varchar(256) NOT NULL UNIQUE,
--     --
--     created_at timestamp DEFAULT now() NOT NULL,
--     updated_at timestamp,
--     deleted_at timestamp,
--     --
--     CONSTRAINT role_pk PRIMARY KEY (id)
-- );

-- CREATE TABLE user_role(
--     id uuid DEFAULT gen_random_uuid() NOT NULL,
--     user_id uuid NOT NULL,
--     role_id uuid NOT NULL,
--     --
--     created_at timestamp DEFAULT now() NOT NULL,
--     updated_at timestamp,
--     deleted_at timestamp,
--     --
--     CONSTRAINT user_role_pk PRIMARY KEY (id),
--     CONSTRAINT user_role_user_fk FOREIGN KEY (user_id) REFERENCES "user"(id),
--     CONSTRAINT user_role_role_fk FOREIGN KEY (role_id) REFERENCES role(id)
-- );

-- CREATE TABLE functionality(
--     id uuid DEFAULT gen_random_uuid() NOT NULL,
--     code varchar(256) NOT NULL UNIQUE,
--     name varchar(256) NOT NULL,
--     --
--     created_at timestamp DEFAULT now() NOT NULL,
--     updated_at timestamp,
--     deleted_at timestamp,
--     --
--     CONSTRAINT functionality_pk PRIMARY KEY (id)
-- );

-- CREATE TABLE role_functionality(
--     id uuid DEFAULT gen_random_uuid() NOT NULL,
--     role_id uuid NOT NULL,
--     functionality_id uuid NOT NULL,
--     --
--     created_at timestamp DEFAULT now() NOT NULL,
--     updated_at timestamp,
--     deleted_at timestamp,
--     --
--     CONSTRAINT role_functionality_pk PRIMARY KEY (id),
--     CONSTRAINT role_functionality_role_fk FOREIGN KEY (role_id) REFERENCES role(id),
--     CONSTRAINT role_functionality_functionality_fk FOREIGN KEY (functionality_id) REFERENCES functionality(id)
-- );

CREATE TABLE user_scope(
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    department_id uuid NOT NULL,
    direction varchar(2) NOT NULL, -- <, >, =, <=, >=
    --
    created_at timestamp DEFAULT now() NOT NULL,
    updated_at timestamp,
    deleted_at timestamp,
    --
    CONSTRAINT user_scope_pk PRIMARY KEY (id),
    CONSTRAINT user_scope_user_fk FOREIGN KEY (user_id) REFERENCES "user"(id),
    CONSTRAINT user_scope_department_fk FOREIGN KEY (department_id) REFERENCES department(id)
);

-- Seed data

INSERT INTO model (name, is_default) VALUES ('mistral', true), ('gpt-4o-mini', false);

INSERT INTO department (code, name) VALUES ('TEC', 'Tecnología');
INSERT INTO department (code, name) VALUES ('TH', 'Talento Humano');
INSERT INTO department (code, name) VALUES ('CRE', 'Créditos');
INSERT INTO department (code, name) VALUES ('SGN', 'Subgerencia de Negocios');

-- INSERT INTO role (name) VALUES ('admin');
-- INSERT INTO role (name) VALUES ('user');

-- INSERT INTO functionality (code, name) VALUES ('chat', 'Chat');

-- INSERT INTO functionality (code, name) VALUES ('user.get', 'Obtener usuarios');
-- INSERT INTO functionality (code, name) VALUES ('user.update', 'Actualizar usuario');
-- INSERT INTO functionality (code, name) VALUES ('user.delete', 'Eliminar usuario');

-- INSERT INTO functionality (code, name) VALUES ('report', 'Reportes');

-- INSERT INTO role_functionality (role_id, functionality_id) 
-- VALUES 
--     ((SELECT id FROM role WHERE name = 'admin'), (SELECT id FROM functionality WHERE code = 'chat')),
--     ((SELECT id FROM role WHERE name = 'admin'), (SELECT id FROM functionality WHERE code = 'user.get')),
--     ((SELECT id FROM role WHERE name = 'admin'), (SELECT id FROM functionality WHERE code = 'user.update')),
--     ((SELECT id FROM role WHERE name = 'admin'), (SELECT id FROM functionality WHERE code = 'user.delete')),
--     ((SELECT id FROM role WHERE name = 'admin'), (SELECT id FROM functionality WHERE code = 'report'));

-- INSERT INTO role_functionality (role_id, functionality_id)
-- VALUES 
--     ((SELECT id FROM role WHERE name = 'user'), (SELECT id FROM functionality WHERE code = 'chat'));

--

INSERT INTO "user" (full_name, email) 
VALUES ('Luis Fernando', 'luis.fernando@example.com');

INSERT INTO "user" (full_name, email)
VALUES ('Ana Gómez', 'ana.gomez@example.com');

-- INSERT INTO user_role (user_id, role_id)
-- VALUES
--     ((SELECT id FROM "user" WHERE email = 'luis.fernando@example.com'), (SELECT id FROM role WHERE name = 'admin')),
--     ((SELECT id FROM "user" WHERE email = 'ana.gomez@example.com'), (SELECT id FROM role WHERE name = 'user'));

-- INSERT INTO user_scope (user_id, department_id, direction)
-- VALUES
--     ((SELECT id FROM "user" WHERE email = 'luis.fernando@example.com'), (SELECT id FROM department WHERE code = 'TEC'), '<='),
--     ((SELECT id FROM "user" WHERE email = 'ana.gomez@example.com'), (SELECT id FROM department WHERE code = 'TH'), '<=');

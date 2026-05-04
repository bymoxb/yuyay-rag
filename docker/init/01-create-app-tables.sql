
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
    --
    created_at timestamp DEFAULT now() NOT NULL,
    updated_at timestamp,
    deleted_at timestamp,
    --
    CONSTRAINT user_pk PRIMARY KEY (id)

);

CREATE TABLE chat(
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    title text NOT NULL,
    user_id uuid NOT NULL,
    department_id uuid,
    model_id uuid,
    rating smallint,
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
    "role" varchar(50) NOT NULL, -- user, assistant, system,
    latency integer NOT NULL DEFAULT 0, -- in milliseconds
    tokens_prompt integer NOT NULL DEFAULT 0,
    tokens_completion integer NOT NULL DEFAULT 0,
    retrieval_context jsonb,
    rating smallint,
    --
    created_at timestamp DEFAULT now() NOT NULL,
    updated_at timestamp,
    deleted_at timestamp,
    --
    CONSTRAINT message_pk PRIMARY KEY (id),
    CONSTRAINT message_chat_fk FOREIGN KEY (chat_id) REFERENCES chat(id),
    CONSTRAINT message_user_fk FOREIGN KEY (user_id) REFERENCES "user"(id)
);


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

INSERT INTO "user" (full_name, email) 
VALUES ('Luis Fernando', 'luis.fernando@example.com');

INSERT INTO "user" (full_name, email)
VALUES ('Ana Gómez', 'ana.gomez@example.com');

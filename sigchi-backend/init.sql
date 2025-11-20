-- Crear la tabla "roles" si no existe
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Insertar roles de ejemplo (admin, doctor, user)
INSERT INTO roles (name)
VALUES
    ('admin'),
    ('doctor'),
    ('user')
ON CONFLICT (name) DO NOTHING;

-- Crear la tabla "users" si no existe
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Insertar usuarios de ejemplo, con contraseñas cifradas (ajustar las contraseñas)
-- Asegúrate de reemplazar los valores de "hashed_password" por contraseñas cifradas reales.
INSERT INTO users (email, hashed_password, first_name, last_name, role_id)
VALUES
    ('admin@example.com', 'admin', 'Admin', 'User', 1),
    ('doctor@example.com', 'doctor', 'John', 'Doe', 2),
    ('user@example.com', 'user', 'Jane', 'Doe', 3)
ON CONFLICT (email) DO NOTHING;

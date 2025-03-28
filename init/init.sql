-- 🛠️ Création des tables pour le système de suivi de course
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 📍 Table des checkpoints
CREATE TABLE checkpoints (
    id SERIAL PRIMARY KEY,
    position VARCHAR(50),
    admin_station_name VARCHAR(50),
    type_of_camera VARCHAR(50),
    is_starting_checkpoint BOOLEAN NOT NULL DEFAULT FALSE
);

-- 🏃‍♂️ Table des participants
CREATE TABLE participant_data (
    id SERIAL PRIMARY KEY,
    id_runner INTEGER UNIQUE NOT NULL,
    pseudo VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 📷 Table des données brutes issues de l'IA
CREATE TABLE raw_data_income_ia (
    id SERIAL PRIMARY KEY,
    checkpoint_id INTEGER REFERENCES checkpoints(id) ON DELETE CASCADE,
    is_starting_checkpoint BOOLEAN NOT NULL DEFAULT FALSE,
    income_id_runner INTEGER,
    image_id VARCHAR(255) NOT NULL,
    last_time_saw_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    treated_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    is_treated BOOLEAN DEFAULT FALSE,
    is_noise_data BOOLEAN DEFAULT FALSE
);

-- 🔁 Index pour accélérer les traitements
CREATE INDEX idx_raw_treated ON raw_data_income_ia (is_treated);
CREATE INDEX idx_raw_runner ON raw_data_income_ia (income_id_runner);
CREATE INDEX idx_raw_noise ON raw_data_income_ia (is_noise_data);

-- 🧠 Table des données consolidées pour affichage/statistiques
CREATE TABLE runner_status (
    id SERIAL PRIMARY KEY,
    id_runner INTEGER NOT NULL REFERENCES participant_data(id_runner) ON DELETE CASCADE,
    id_raw_data INTEGER REFERENCES raw_data_income_ia(id) ON DELETE SET NULL,
    checkpoint_id INTEGER REFERENCES checkpoints(id),
    is_starting_checkpoint BOOLEAN NOT NULL DEFAULT FALSE,
    amount_of_laps_runned INTEGER DEFAULT 0,
    average_speed FLOAT,
    total_time_runned INTEGER,
    runner_current_position INTEGER,
    time_spend_current_lap INTEGER,
    last_time_saw_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    has_shown_in_front BOOLEAN DEFAULT FALSE
);

-- Index pour le traitement frontal
CREATE INDEX idx_runner_shown ON runner_status (has_shown_in_front);

-- Creation des checkpoints
INSERT INTO checkpoints (id, position, admin_station_name, is_starting_checkpoint)
VALUES (1, 'Poste A', 'Checkpoint Principal', TRUE);

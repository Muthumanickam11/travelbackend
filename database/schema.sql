CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    preferences JSONB DEFAULT '{}'
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    date TIMESTAMP,
    cost DECIMAL(10, 2),
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE itineraries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    events JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

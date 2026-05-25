-- The Acutis API - Database Schema (PostgreSQL)

-- 1. POPES TABLE
-- Note: saint_id foreign key constraint is added later to avoid circular dependency
CREATE TABLE popes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    succession_number INT NOT NULL,
    papal_name VARCHAR(100) NOT NULL,
    baptism_name VARCHAR(150) NOT NULL,
    nationality VARCHAR(100) NOT NULL,
    religious_order VARCHAR(100),
    papal_motto VARCHAR(255),
    pontificate_start DATE NOT NULL,
    pontificate_end DATE,
    end_reason VARCHAR(50),
    saint_id UUID
);

-- 2. SAINTS TABLE
CREATE TABLE saints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    official_name VARCHAR(150) NOT NULL,
    baptism_name VARCHAR(150),
    gender VARCHAR(1) CHECK (gender IN ('M', 'F')),
    current_status VARCHAR(50) NOT NULL,
    vocation VARCHAR(100),
    civil_occupation VARCHAR(100),
    feast_day INT CHECK (feast_day >= 1 AND feast_day <= 31),
    feast_month INT CHECK (feast_month >= 1 AND feast_month <= 12),
    birth_date DATE,
    birth_place VARCHAR(100),
    region_of_activity VARCHAR(150),
    death_date DATE,
    death_place VARCHAR(100),
    veneration_date DATE,
    venerated_by_pope_id UUID REFERENCES popes(id),
    beatification_date DATE,
    beatified_by_pope_id UUID REFERENCES popes(id),
    canonization_date DATE,
    canonized_by_pope_id UUID REFERENCES popes(id),
    is_doctor_of_church BOOLEAN DEFAULT FALSE,
    profile_image_url VARCHAR(255),
    short_bio VARCHAR(500),
    full_bio TEXT
);

-- Resolving the circular dependency: Add the FK from popes to saints
ALTER TABLE popes
ADD CONSTRAINT fk_pope_saint
FOREIGN KEY (saint_id) REFERENCES saints(id);

-- 3. PATRONAGES
CREATE TABLE patronage_causes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cause_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL
);

CREATE TABLE saint_patronage (
    saint_id UUID REFERENCES saints(id) ON DELETE CASCADE,
    cause_id UUID REFERENCES patronage_causes(id) ON DELETE CASCADE,
    justification TEXT,
    PRIMARY KEY (saint_id, cause_id)
);

-- 4. MIRACLES TABLE
CREATE TABLE miracles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    saint_id UUID REFERENCES saints(id) ON DELETE SET NULL,
    title VARCHAR(150) NOT NULL,
    miracle_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    occurrence_year INT,
    approval_date DATE,
    city VARCHAR(100),
    country VARCHAR(100),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8)
);

-- 5. PERFORMANCE INDEXES
CREATE INDEX idx_saints_name ON saints(official_name);
CREATE INDEX idx_saints_status ON saints(current_status);
CREATE INDEX idx_miracles_type ON miracles(miracle_type);
CREATE INDEX idx_causes_category ON patronage_causes(category);
CREATE DATABASE news_geo;
\c news_geo;

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE news_articles (
    id TEXT PRIMARY KEY,
    county TEXT,
    state TEXT,
    country TEXT,
    title TEXT NOT NULL,
    published_utc TIMESTAMPTZ NOT NULL,
    source TEXT,
    url TEXT UNIQUE,
    summary TEXT,
    raw JSONB,
    location_name TEXT,
    geom GEOMETRY(POINT, 4326),
    category TEXT,
    actionable BOOLEAN DEFAULT FALSE,
    extracted_claims TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for fast queries:
CREATE INDEX idx_news_published ON news_articles(published_utc DESC);
CREATE INDEX idx_news_geom ON news_articles USING GIST (geom);
CREATE INDEX idx_news_category ON news_articles(category);


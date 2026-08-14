CREATE TABLE jobs (
    source        TEXT NOT NULL,
    external_id   TEXT NOT NULL,
    title         TEXT NOT NULL,
    location      TEXT,
    url           TEXT NOT NULL,
    company       TEXT,
    posted_at     TEXT,
    raw_json      JSONB,
    description   TEXT,
    skills TEXT[],
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at     TIMESTAMPTZ,
    PRIMARY KEY (source, external_id)
);
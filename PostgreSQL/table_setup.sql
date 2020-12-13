CREATE DATABASE annotation;

CREATE USER annotator WITH PASSWORD 'annotation';

GRANT ALL PRIVILEGES ON DATABASE annotation TO annotator;


CREATE TABLE batches(
    batch_ID VARCHAR(255) PRIMARY KEY,
    paragraph_IDs TEXT[]
);

CREATE TABLE annotations(
    batch_ID  VARCHAR(255),
    paragraph_ID VARCHAR(255),
    answer_time timestamp,
    annotations TEXT[],
    PRIMARY KEY (batch_ID, paragraph_ID, answer_time)
);

CREATE TABLE paragraphs (
    paragraph_ID VARCHAR(255) PRIMARY KEY,
    article_URL VARCHAR(255),
    paragraph_content TEXT
);
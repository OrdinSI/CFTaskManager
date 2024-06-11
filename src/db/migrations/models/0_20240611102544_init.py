from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "subjects" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "tag" VARCHAR(30) NOT NULL UNIQUE,
    "name" VARCHAR(100) NOT NULL UNIQUE
);
COMMENT ON TABLE "subjects" IS 'Model for task subjects (tags)';
CREATE TABLE IF NOT EXISTS "tasks" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL,
    "number" VARCHAR(30)  UNIQUE,
    "solved_count" BIGINT NOT NULL  DEFAULT 0,
    "rating" BIGINT NOT NULL  DEFAULT 0,
    "url" VARCHAR(150) NOT NULL,
    "used_in_contest" BOOL NOT NULL  DEFAULT False
);
COMMENT ON TABLE "tasks" IS 'Model for tasks';
CREATE TABLE IF NOT EXISTS "contests" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "subject_id" BIGINT NOT NULL REFERENCES "subjects" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "contests" IS 'Model for contests';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "tasks_subjects" (
    "tasks_id" BIGINT NOT NULL REFERENCES "tasks" ("id") ON DELETE CASCADE,
    "subject_id" BIGINT NOT NULL REFERENCES "subjects" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_tasks_subje_tasks_i_629587" ON "tasks_subjects" ("tasks_id", "subject_id");
CREATE TABLE IF NOT EXISTS "contests_tasks" (
    "contests_id" BIGINT NOT NULL REFERENCES "contests" ("id") ON DELETE CASCADE,
    "task_id" BIGINT NOT NULL REFERENCES "tasks" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_contests_ta_contest_226359" ON "contests_tasks" ("contests_id", "task_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """

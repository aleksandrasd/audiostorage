CREATE TABLE "user" (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    nickname VARCHAR(255) NOT NULL UNIQUE,
    is_admin BOOLEAN,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE user_raw_uploaded_file (
   id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
   "user_id" BIGINT REFERENCES "user"(id) ON DELETE CASCADE,
   "file_name" TEXT NOT NULL,
   "original_file_name" TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_user_raw_uploaded_file_created_at ON "user_raw_uploaded_file" (created_at);

CREATE TYPE audio_type AS ENUM ('mp3', 'wav');

CREATE TABLE "audio_file_meta" (
   id BIGSERIAL PRIMARY KEY,
   length_in_seconds INT4
);

CREATE TABLE "audio_file" (
   id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
   meta_id  BIGSERIAL REFERENCES audio_file_meta(id) ON DELETE CASCADE,
   bucket TEXT NOT NULL,
   "file_name" TEXT NOT NULL UNIQUE,
   file_type "audio_type",
   file_size_in_bytes BIGINT
);
COMMENT ON TABLE audio_file IS 'Contains metadata of every audio file that was uploaded or created. Audio files are created after converting uploaded audio files into formats that project supports.';


CREATE TABLE "user_audio_file" (
   "user_id" BIGINT REFERENCES "user"(id) ON DELETE CASCADE,
   "audio_file_id"  UUID REFERENCES "audio_file"(id)  ON DELETE CASCADE,
   "upload_id" BIGINT REFERENCES "user_raw_uploaded_file"(id),
   CONSTRAINT un_c_user_audio_file_user_id_audio_file_id UNIQUE ("user_id", "audio_file_id")
);

CREATE TABLE "policy" (
	upload_max_size_in_bytes BIGINT NOT NULL,
	audio_formats_download VARCHAR(10) ARRAY NOT NULL
);
INSERT INTO "policy"(upload_max_size_in_bytes, audio_formats_download) VALUES (1073741824, '{mp3, wav}');

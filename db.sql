CREATE OR REPLACE FUNCTION tokenize_filename(filename TEXT)
RETURNS TEXT AS $$
DECLARE
    clean_name TEXT;
    tokens TEXT[];
    temp_tokens TEXT[];
    temp_token TEXT;
BEGIN
    -- Replace non-alphanumeric characters with spaces except dots and underscores
    clean_name := regexp_replace(filename, '[^a-zA-Z0-9._]', ' ', 'g');

    -- Split by spaces, underscores, and dots
    temp_tokens := regexp_split_to_array(clean_name, '[ _\.]');

    -- Generate additional tokens (e.g., extracting numbers and base words)
    FOREACH temp_token IN ARRAY temp_tokens LOOP
        tokens := array_append(tokens, temp_token);

        -- Extract number parts
        IF temp_token ~ '^[0-9]+$' THEN
            CONTINUE;
        END IF;

        -- Extract trailing numbers
        IF temp_token ~ '[0-9]$' THEN
            tokens := array_append(tokens, regexp_replace(temp_token, '^[^0-9]*', '', 'g'));
        END IF;

        -- Extract leading letters
        IF temp_token ~ '^[a-zA-Z]+' THEN
            tokens := array_append(tokens, regexp_replace(temp_token, '[0-9].*$', '', 'g'));
        END IF;
    END LOOP;

    -- Remove duplicates and empty values
    RETURN string_agg(unnest, ' ' ORDER BY ordinality)
		FROM (
		    SELECT DISTINCT ON (unnest) unnest, ordinality
		    FROM unnest(tokens) WITH ORDINALITY AS t(unnest, ordinality)
		    WHERE unnest IS NOT NULL AND unnest <> ''
		    ORDER BY unnest, ordinality
		) subquery;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

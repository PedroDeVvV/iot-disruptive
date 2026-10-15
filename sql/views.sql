CREATE OR REPLACE VIEW avg_temp_por_ambiente AS
SELECT
    location,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temp,
    COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY location
ORDER BY location;

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM recorded_at)::integer AS hora,
    COUNT(*) AS contagem,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temp
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM recorded_at)
ORDER BY hora;

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    recorded_at::date AS data,
    MAX(temperature) AS temp_max,
    MIN(temperature) AS temp_min,
    ROUND(AVG(temperature)::numeric, 2) AS temp_media,
    MAX(temperature) - MIN(temperature) AS amplitude_termica
FROM temperature_readings
GROUP BY recorded_at::date
ORDER BY data;

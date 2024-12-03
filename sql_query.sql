SELECT text, by, TIMESTAMP_SECONDS(time) as timestamp
FROM `bigquery-public-data.hacker_news.full`
WHERE text IS NOT NULL
LIMIT 5

psql "dbname=news_geo user=postgres host=localhost port=5432" \
  -c "\COPY (
        SELECT
          id, title, county, state, country, source, url, summary,
          published_utc AS timestamp, category, actionable, extracted_claims,
          ST_X(geom)::numeric(9,6) AS lon,
          ST_Y(geom)::numeric(9,6) AS lat,
          ST_AsText(geom)          AS geometry
        FROM public.news_articles
        WHERE geom IS NOT NULL
      ) TO STDOUT WITH (FORMAT CSV, HEADER, ENCODING 'UTF8');" | gzip > news_articles_kepler.csv.gz

---

psql "dbname=news_geo user=postgres host=localhost port=5432" \
  -c "\COPY (
        SELECT
          id,
          title,
          county,
          state,
          country,
          source,
          url,
          summary,
          published_utc          AS timestamp,      -- Kepler time column
          category,
          actionable,
          extracted_claims,
          ST_X(geom)::numeric(9,6) AS lon,          -- longitude (EPSG 4326)
          ST_Y(geom)::numeric(9,6) AS lat,          -- latitude
          ST_AsText(geom)          AS geometry      -- WKT backup
        FROM   public.news_articles
        WHERE  geom IS NOT NULL
      ) TO '/tmp/news_articles_kepler.csv'
      WITH (FORMAT CSV, HEADER, ENCODING 'UTF8');"


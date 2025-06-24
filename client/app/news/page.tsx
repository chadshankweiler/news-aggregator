// app/news/page.tsx  (server component)
import { Pool } from 'pg'
import NewsClient from './_components/newsclient'

export const revalidate = 300             // ISR – refresh DB read every 5 min

type Article = {
  id: string
  county: string
  title: string
  source: string
  url: string
  published_utc: string
}

async function getAllNews(): Promise<Article[]> {
  const pool = new Pool({ connectionString: 'postgres://postgres:lol@localhost:5432/postgres'})
  const { rows } = await pool.query<Article>(
    `SELECT id, county, title, source, url, published_utc
       FROM news_articles
      ORDER BY published_utc DESC`
  )
  await pool.end()
  return rows
}

export default async function AllNewsPage() {
  const articles = await getAllNews()
  return <NewsClient initial={articles} />
}


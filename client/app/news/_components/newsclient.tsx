'use client'
import { useMemo, useState } from 'react'

type Article = {
  id: string
  county: string
  title: string
  source: string
  url: string
  published_utc: string
}

export default function NewsClient({ initial }: { initial: Article[] }) {
  const [county, setCounty] = useState<string>('ALL')

  // list of distinct counties for the <select>
  const counties = useMemo(
    () =>
      Array.from(new Set(initial.map(a => a.county))).sort((a, b) =>
        a.localeCompare(b)
      ),
    [initial]
  )

  // client-side filter
  const visible = useMemo(
    () =>
      county === 'ALL' ? initial : initial.filter(a => a.county === county),
    [county, initial]
  )

  return (
    <main className="mx-auto max-w-4xl p-6 space-y-6">
      {/* filter bar */}
      <div className="flex items-center gap-3">
        <label htmlFor="county" className="font-medium">
          County:
        </label>
        <select
          id="county"
          value={county}
          onChange={e => setCounty(e.target.value)}
          className="border px-2 py-1 rounded"
        >
          <option value="ALL">All ( {initial.length} )</option>
          {counties.map(c => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
        <span className="text-sm text-gray-600">
          Showing {visible.length} article{visible.length !== 1 ? 's' : ''}
        </span>
      </div>

      {/* list */}
      <ul className="space-y-4">
        {visible.map(a => (
          <li key={a.id} className="border-b pb-3">
            <a
              href={a.url}
              target="_blank"
              className="text-blue-600 hover:underline"
            >
              {a.title}
            </a>
            <div className="text-sm text-gray-600">
              {a.county} • {a.source} •{' '}
              {new Date(a.published_utc).toLocaleString()}
            </div>
          </li>
        ))}
      </ul>
    </main>
  )
}


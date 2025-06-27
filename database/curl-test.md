curl -X POST http://192.168.1.197:5000/news \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "county": "Miami-Dade County",
      "state": "Florida",
      "country": "United States",
      "date_from": "2025-06-25T00:00:00Z",
      "date_to": "2025-06-26T00:00:00Z",
      "generated_utc": "2025-06-26T00:00:00Z"
    },
    "articles": [
      {
        "id": "76a8b5b2d8e9f123c4567890abcdef1234567890",
        "title": "Police seek man with Cuban accent in Little Havana knife robbery",
        "published_utc": "2025-06-25T16:46:00Z",
        "source": "CiberCuba (Miami News)",
        "url": "https://en.cibercuba.com/noticias/2025-06-25-u1-e129488-s27061-nid305786-piden-ayuda-identificar-hombre-acento-cubano-llevo",
        "summary": "Miami police released images of a Hispanic man, 65–68, with a Cuban accent who threatened an employee with a knife at a travel agency in Little Havana on June 2. They stole cash and a $5,000 bracelet. Public assistance is requested.",
        "location": {
          "lat": 25.7650,
          "lon": -80.2230
        }
      },
      {
        "id": "d4f2e3c5a6b7980123456789abcdef012345678",
        "title": "Woman dragged from Miami‑Dade commission meeting protesting ICE agreement",
        "published_utc": "2025-06-26T02:00:00Z",
        "source": "NBC Miami",
        "url": "https://www.nbcmiami.com/news/local/woman-dragged-from-miami-dade-commission-meeting-protesting-ice-agreement/3646137/",
        "summary": "During a June 26 Miami‑Dade County Commission meeting at Stephen P. Clark Center in downtown Miami, deputies forcibly removed protester Camila Ramos over objection to an ICE‑jail agreement; she faces charges.",
        "location": {
          "lat": 25.7740,
          "lon": -80.1940
        }
      }
    ]
  }'


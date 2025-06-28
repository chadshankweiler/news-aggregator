'use client';

import dynamic from 'next/dynamic';
import React from 'react';

const DynamicConnectedKeplerGlClient = dynamic<any>(
    () => import('./_components/kepler-client'),
    {
        ssr: false,
        loading: () => <p>Loading map...</p>,
    }
);

export default function HomePage() {
    const MAPBOX_TOKEN = process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN;
    const initialData = [
      {
        info: {
          label: 'My Geo Data',
          id: 'my_data',
        },
        data: {
          fields: [ { id: 'latitude', type: 'real' }, { id: 'longitude', type: 'real' }, { id: 'value', type: 'real' } ],
          rows: [ [ 35.68, 139.76, 100 ], [ 34.05, -118.24, 200 ] ],
        },
      }
    ];

    const initialConfig = {
      version: 'v1',
      config: {
         mapState: { latitude: 35.68, longitude: 139.76, zoom: 8 },
        }
    };

    return (
        <div style={{ width: '100vw', height: '100vh', overflow: 'hidden' }}>
            <DynamicConnectedKeplerGlClient
                mapboxApiAccessToken={'pk.eyJ1IjoiY2hhZHNoYW5rd2VpbGVyIiwiYSI6ImNtY2V5OHNtdDAyd3MycXB4N2ZranNlNjQifQ.MqucuIPjJd_J0qq_iaR5Ug'}
                id="mymap"
                initialData={initialData}
                initialConfig={initialConfig}
            />
        </div>
    );
}

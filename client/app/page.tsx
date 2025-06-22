// pages/map.tsx   (or app/map/page.tsx)
"use client";
import dynamic from "next/dynamic";

const LeafletMap = dynamic(() => import("@/app/_components/leafletmap"), {
    ssr: false,
});

export default function MapPage() {
    return (
        <div style={{ height: "100vh", width: "50vw" }}>
            <LeafletMap />
        </div>
    );
}

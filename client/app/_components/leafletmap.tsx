// components/LeafletMap.tsx
"use client";
import { GeoJSON, MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useState } from "react";

// Fix missing default marker icons
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
    iconUrl: require("leaflet/dist/images/marker-icon.png"),
    shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

export default function LeafletMap() {
    const center: [number, number] = [25.684, -80.36];
    const florida: [number, number] = [25.887568, -80.181045];

    const [shape, setShape] = useState<any | null>(null);

    useEffect(() => {
        fetch("/florida.json")
            .then((r) => r.json())
            .then((json) => setShape(json)); // 1-feature FeatureCollection
    }, []);
    
    console.log(shape)

    return (
        <MapContainer
            center={florida}
            zoom={13}
            style={{ height: "100%", width: "100%" }}
        >
            <TileLayer
                attribution="&copy; OpenStreetMap contributors"
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <Marker position={florida}>
                <Popup>Hello from Leaflet in Next.js</Popup>
            </Marker>
            {/* red outline, no fill */}
            {shape && shape.features.map((feat: any, idx) =>(
                <GeoJSON
                    key={idx}
                    data={feat}
                    style={{ color: "red", weight: 2, fill: true }}
                />
            ))}
            <MinimapControl position="topright" />
        </MapContainer>
    );
}

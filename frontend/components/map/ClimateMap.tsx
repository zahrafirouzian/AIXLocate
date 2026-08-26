"use client";


import {

    MapContainer,

    TileLayer,

    Marker,

    Popup

} from "react-leaflet";


import "leaflet/dist/leaflet.css";


import L from "leaflet";



// Fix leaflet icons

delete (L.Icon.Default.prototype as any)._getIconUrl;


L.Icon.Default.mergeOptions({

    iconRetinaUrl:
        "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",

    iconUrl:
        "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",

    shadowUrl:
        "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",

});




export default function ClimateMap(

    {
        locations
    }:
    {
        locations:any[]
    }

){


    const center:[number,number] = [

        33.4484,

        -112.0740

    ];



    return (

        <div className="mt-8 h-[500px] rounded-xl overflow-hidden">


            <MapContainer

                center={center}

                zoom={11}

                style={{

                    height:"100%",

                    width:"100%"

                }}

            >


                <TileLayer

                    attribution='&copy; OpenStreetMap'

                    url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"

                />



                {

                    locations.map(

                        (location)=>(


                            <Marker

                                key={location.name}

                                position={[

                                    location.lat,

                                    location.lon

                                ]}

                            >


                                <Popup>


                                    <div>


                                        <h3 className="font-bold">

                                            {location.name}

                                        </h3>



                                        <p>

                                            Score:

                                            {" "}

                                            {location.suitability_score}

                                        </p>



                                        <p>

                                            Temperature:

                                            {" "}

                                            {location.temperature} °C

                                        </p>



                                    </div>


                                </Popup>


                            </Marker>


                        )

                    )

                }



            </MapContainer>


        </div>

    );

}

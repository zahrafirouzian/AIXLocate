"use client";


export default function RankingBar(

    {
        locations
    }:
    {
        locations:any[]
    }

){


    return (

        <div className="mt-8 rounded-xl border p-6">


            <h2 className="text-2xl font-bold mb-5">

                Location Ranking

            </h2>



            <div className="space-y-5">


                {

                    locations

                    .sort(

                        (a,b)=>

                        b.suitability_score -

                        a.suitability_score

                    )

                    .map(

                        (location,index)=>(


                            <div key={location.name}>


                                <div className="flex justify-between mb-2">


                                    <span className="font-semibold">

                                        {index+1}.

                                        {" "}

                                        {location.name}

                                    </span>



                                    <span>

                                        {location.suitability_score}/100

                                    </span>


                                </div>





                                <div className="h-4 rounded bg-gray-200">


                                    <div

                                        className="h-4 rounded bg-green-500"

                                        style={{

                                            width:

                                            `${location.suitability_score}%`

                                        }}

                                    />


                                </div>


                            </div>


                        )

                    )

                }


            </div>


        </div>

    );

}

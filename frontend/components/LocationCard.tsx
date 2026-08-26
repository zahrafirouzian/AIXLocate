export default function LocationCard(

{
location
}:
{
location:any
}

){


const recommended =

location.suitability_score ===

Math.max(

location.suitability_score

);



return (

<div className="rounded-xl border p-6 shadow">


<div className="flex justify-between">


<h2 className="text-xl font-bold">

{location.name}

</h2>



{

location.suitability_score > 50 &&

<span className="rounded bg-green-100 px-3 py-1">

🏆 Recommended

</span>

}


</div>





<div className="mt-4 space-y-2">


<p>

🌡 Temperature:

{" "}

{location.temperature}°C

</p>


<p>

☀ Solar GHI:

{" "}

{location.solar_ghi}

</p>


<p>

🔆 Solar DNI:

{" "}

{location.solar_dni}

</p>


<p>

❄ Cooling:

{" "}

{location.cooling_score}

</p>


<p>

🔥 Thermal:

{" "}

{location.thermal_score}

</p>


<p className="font-bold">

⭐ Suitability:

{" "}

{location.suitability_score}

</p>



</div>



</div>

);


}
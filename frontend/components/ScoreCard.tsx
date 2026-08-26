export default function ScoreCard(

{
score
}:
{
score:number
}

){


const level =

score >= 70

?

"Excellent"

:

score >= 50

?

"Good"

:

"Poor";



return (

<div className="rounded-xl border p-6 shadow">


<h3 className="text-xl font-bold">

AI Data Center Suitability

</h3>



<p className="mt-4 text-5xl font-bold">

{score}

<span className="text-2xl">

/100

</span>

</p>



<p className="mt-3 text-lg">

Status:

{" "}

<span className="font-bold">

{level}

</span>

</p>


</div>

);


}
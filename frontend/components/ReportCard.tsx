export default function ReportCard(
    {
        report
    }:
    {
        report:string
    }
){

    return (

        <div className="rounded-xl bg-gray-100 p-6 mt-6">

            <h2 className="text-xl font-bold mb-3">
                AI Analysis Report
            </h2>


            <p className="whitespace-pre-line">
                {report}
            </p>


        </div>

    );

}

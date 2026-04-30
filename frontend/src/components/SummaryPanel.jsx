export default function SummaryPanel({

  sentiment,

  followup,

  product

}) {

  return (

    <div className="bg-violet-50 border border-violet-200 rounded-xl p-4 mt-6">

      <h3 className="font-semibold text-violet-800 mb-3">
        AI Summary
      </h3>

      <div className="space-y-2 text-sm">

        <p>
          <strong>Product:</strong> {product}
        </p>

        <p>
          <strong>Sentiment:</strong> {sentiment}
        </p>

        <p>
          <strong>Follow-up:</strong> {followup}
        </p>

      </div>

    </div>
  )
}
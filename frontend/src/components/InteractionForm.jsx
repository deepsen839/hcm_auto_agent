import {
  Calendar,
  Clock3
} from 'lucide-react'

export default function InteractionForm({

  hcpName,
  product,
  sentiment,
  topics,
  outcomes,
  followup,

  setInteractionData,

  dispatch,

  date,

  time,

  interactionType,
  setInteractionType

}){

  return (

    <div className="lg:col-span-8 bg-white rounded-2xl border border-gray-200 shadow-sm p-6 overflow-y-auto">

      <h2 className="text-lg font-semibold mb-6 text-gray-700">
        Interaction Details
      </h2>

      {/* HCP + TYPE */}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">

        <div>

          <label className="text-sm text-gray-600 block mb-2">
            HCP Name
          </label>

          <input
            type="text"
            value={hcpName}
            onChange={(e) =>
              dispatch(
                setInteractionData({
                  hcpName:
                    e.target.value
                })
              )
            }
            placeholder="Search or select HCP..."
            className="w-full border border-gray-300 rounded-lg px-4 py-3"
          />

        </div>

        <div>

          <label className="text-sm text-gray-600 block mb-2">
            Interaction Type
          </label>

          <select
            value={interactionType}
            onChange={(e) =>
              setInteractionType(
                e.target.value
              )
            }
            className="w-full border border-gray-300 rounded-lg px-4 py-3"
          >

            <option>Meeting</option>
            <option>Call</option>
            <option>Email</option>

          </select>

        </div>

      </div>

      {/* PRODUCT */}

      <div className="mb-4">

        <label className="text-sm text-gray-600 block mb-2">
          Product
        </label>

        <input
          type="text"
          value={product}
          onChange={(e) =>
            dispatch(
              setInteractionData({
                product:
                  e.target.value
              })
            )
          }
          className="w-full border border-gray-300 rounded-lg px-4 py-3"
        />

      </div>

      {/* DATE + TIME */}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">

        <div>

          <label className="text-sm text-gray-600 block mb-2">
            Date
          </label>

          <div className="relative">

            <Calendar className="absolute left-3 top-3.5 w-4 h-4 text-gray-400" />

            <input
              type="date"
              value={date}
              onChange={(e) =>
                        dispatch(
                          setInteractionData({
                            date: e.target.value
                          })
                        )
                      }
              className="w-full border border-gray-300 rounded-lg pl-10 pr-4 py-3"
            />

          </div>

        </div>

        <div>

          <label className="text-sm text-gray-600 block mb-2">
            Time
          </label>

          <div className="relative">

            <Clock3 className="absolute left-3 top-3.5 w-4 h-4 text-gray-400" />

            <input
              type="time"
              value={time}
              onChange={(e) =>
                  dispatch(
                    setInteractionData({
                      time: e.target.value
                    })
                  )
                }
              className="w-full border border-gray-300 rounded-lg pl-10 pr-4 py-3"
            />

          </div>

        </div>

      </div>

      {/* TOPICS */}

      <textarea
        rows={4}
        value={topics}
        onChange={(e) =>
          dispatch(
            setInteractionData({
              topics:
                e.target.value
            })
          )
        }
        placeholder="Topics discussed..."
        className="w-full border border-gray-300 rounded-lg px-4 py-3 mb-4"
      />

      {/* OUTCOMES */}

      <textarea
        rows={3}
        value={outcomes}
        onChange={(e) =>
          dispatch(
            setInteractionData({
              outcomes:
                e.target.value
            })
          )
        }
        placeholder="Outcomes..."
        className="w-full border border-gray-300 rounded-lg px-4 py-3 mb-4"
      />

      {/* FOLLOWUP */}

      <textarea
        rows={3}
        value={followup}
        onChange={(e) =>
          dispatch(
            setInteractionData({
              followup:
                e.target.value
            })
          )
        }
        placeholder="Follow-up..."
        className="w-full border border-gray-300 rounded-lg px-4 py-3"
      />

    </div>
  )
}
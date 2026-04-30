import { useState } from 'react'

import {
  useDispatch,
  useSelector
} from 'react-redux'

import {
  setInteractionData
} from '../store/interactionSlice'

import ChatInterface
from '../components/ChatInterface'

import InteractionForm
from '../components/InteractionForm'

import SummaryPanel
from '../components/SummaryPanel'

export default function LogInteraction() {

  const dispatch = useDispatch()
  const {

    hcpName,
    product,
    sentiment,
    topics,
    outcomes,
    followup,
    date,
    time

  } = useSelector(
    state => state.interaction
  )
  // =========================
  // DATE + TIME
  // =========================





  const [interactionType, setInteractionType] =
    useState('Meeting')

  // =========================
  // UI
  // =========================

  return (

    <div className="h-screen overflow-hidden bg-[#f5f6fa] p-6 font-['Inter']">

      <div className="max-w-7xl mx-auto h-full flex flex-col">

        {/* HEADER */}

        <h1 className="text-3xl font-semibold text-left mb-6 text-gray-800">
          Log HCP Interaction
        </h1>

        {/* MAIN GRID */}

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1 min-h-0 overflow-hidden">

          {/* LEFT PANEL */}

          <div className="lg:col-span-8 flex flex-col gap-6 overflow-y-auto">

            <InteractionForm

              hcpName={hcpName}

              product={product}

              sentiment={sentiment}

              topics={topics}

              outcomes={outcomes}

              followup={followup}

              dispatch={dispatch}

              setInteractionData={setInteractionData}

              date={date}


              time={time}


              interactionType={interactionType}

              setInteractionType={setInteractionType}

            />

            <SummaryPanel

              sentiment={sentiment}

              followup={followup}

              product={product}

            />

          </div>

          {/* RIGHT PANEL */}

          <ChatInterface />

        </div>

      </div>

    </div>
  )
}
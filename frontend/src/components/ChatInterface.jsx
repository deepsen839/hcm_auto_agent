import {
  useState,
  useEffect,
  useRef
} from 'react'

import api from '../services/api'

import { store }
from '../store/store'

import {
  useDispatch,
  useSelector
} from 'react-redux'

import {
  addMessage,
  setInteractionData
} from '../store/interactionSlice'

import { Send } from 'lucide-react'

export default function ChatInterface() {

  const [message, setMessage] =
    useState('')

  const dispatch = useDispatch()

  const now = new Date()

  const currentDate =
    now.toISOString().split('T')[0]

  const currentTime =
    now.toTimeString().slice(0, 5)

  const {

    messages

  } = useSelector(
    state => state.interaction
  )

  // =========================
  // AUTO SCROLL
  // =========================

  const messagesEndRef = useRef(null)

  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth'
    })

  }, [messages])

  // =========================
  // SEND MESSAGE
  // =========================

  const sendMessage = async () => {

    if (!message.trim()) return

    // =========================
    // CURRENT REDUX STATE
    // =========================

    const currentState =
      store.getState().interaction

    // =========================
    // USER MESSAGE
    // =========================

    dispatch(addMessage({

      role: 'user',

      text: message

    }))

    try {

      // =========================
      // API CALL
      // =========================

      const response =
        await api.post('/chat', {

          message,

          existing_data: currentState,

          current_datetime:
            new Date().toISOString()

        })

      const data = response.data

      // =========================
      // UPDATE REDUX FORM STATE
      // =========================

      dispatch(setInteractionData({

        hcpName:

          data.interaction.hcp_name ||

          currentState.hcpName,

        product:

          (
            data.interaction.product &&

            data.interaction.product !==
            'Unknown Product'
          )

            ? data.interaction.product

            : currentState.product,

        sentiment:

          data.interaction.sentiment ||

          currentState.sentiment,

        topics:

          data.interaction.summary ||

          currentState.topics,

        outcomes:

          data.interaction.summary ||

          currentState.outcomes,

        followup:

          data.interaction.follow_up_action ||

          currentState.followup,

        date:

          data.interaction.date ||

          currentState.date ||

          currentDate,

        time:

          data.interaction.time ||

          currentState.time ||

          currentTime

      }))

      // =========================
      // AI CHAT MESSAGE
      // =========================

      dispatch(addMessage({

        role: 'assistant',

        text:

          `HCP: ${
            data.interaction.hcp_name ||
            currentState.hcpName
          }\n` +

          `Product: ${
            (
              data.interaction.product &&
              data.interaction.product !==
              'Unknown Product'
            )

              ? data.interaction.product

              : currentState.product
          }\n` +

          `Sentiment: ${
            data.interaction.sentiment ||
            currentState.sentiment
          }\n` +

          `Compliance: ${
            data.compliance.status
          }`

      }))

    } catch (error) {

      console.error(error)

      dispatch(addMessage({

        role: 'assistant',

        text:
          'Backend connection error.'

      }))

    }

    // =========================
    // CLEAR INPUT
    // =========================

    setMessage('')
  }

  return (

    <div className="lg:col-span-4 bg-white rounded-2xl border border-gray-200 shadow-sm flex flex-col h-full overflow-hidden">

      {/* HEADER */}

      <div className="p-4 border-b">

        <h2 className="font-semibold text-gray-800">
          AI Assistant
        </h2>

        <p className="text-sm text-gray-500 mt-1">
          Log interaction via chat
        </p>

      </div>

      {/* MESSAGES */}

      <div className="flex-1 overflow-y-auto p-4 space-y-3">

        {messages.map((msg, idx) => (

          <div
            key={idx}
            className={`flex ${
              msg.role === 'user'
                ? 'justify-end'
                : 'justify-start'
            }`}
          >

            <div
              className={`max-w-[85%] px-4 py-3 rounded-2xl text-sm whitespace-pre-line break-words ${
                msg.role === 'user'
                  ? 'bg-gray-100 text-gray-800'
                  : 'bg-violet-100 text-violet-900'
              }`}
            >

              {msg.text}

            </div>

          </div>

        ))}

        <div ref={messagesEndRef} />

      </div>

      {/* INPUT */}

      <div className="border-t p-4 bg-white">

        <div className="flex items-center gap-3">

          <input

            value={message}

            onChange={(e) =>
              setMessage(e.target.value)
            }

            onKeyDown={(e) => {

              if (e.key === 'Enter') {

                e.preventDefault()

                sendMessage()
              }

            }}

            placeholder="Describe your HCP interaction"

            className="flex-1 min-w-0 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-violet-500"
          />

          <button
            onClick={sendMessage}
            className="shrink-0 bg-violet-600 hover:bg-violet-700 text-white px-5 py-3 rounded-lg flex items-center justify-center transition"
          >

            <Send className="w-4 h-4" />

          </button>

        </div>

      </div>

    </div>
  )
}
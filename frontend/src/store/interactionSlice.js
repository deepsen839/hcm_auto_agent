import { createSlice } from '@reduxjs/toolkit'

const now = new Date()

const initialState = {

  hcpName: '',

  product: '',

  sentiment: 'neutral',

  topics: '',

  outcomes: '',

  followup: '',

  date:
    now.toISOString().split('T')[0],

  time:
    now.toTimeString().slice(0, 5),

  messages: [
    {
      role: 'assistant',
      text:
        'Hello! Describe your HCP interaction.'
    }
  ]
}

const interactionSlice = createSlice({

  name: 'interaction',

  initialState,

  reducers: {

    setInteractionData: (state, action) => {

      Object.assign(state, action.payload)

    },

    addMessage: (state, action) => {

      state.messages.push(action.payload)

    },

    clearMessages: (state) => {

      state.messages = []
    }

  }

})

export const {

  setInteractionData,

  addMessage,

  clearMessages

} = interactionSlice.actions

export default interactionSlice.reducer
import { createSlice } from '@reduxjs/toolkit'

export const authSlice = createSlice({
  name: 'authentication',
  initialState: {
    key: null
  },
  reducers: {
    login: (state, action) => {
      // Redux Toolkit allows us to write "mutating" logic in reducers. It
      // doesn't actually mutate the state because it uses the Immer library,
      // which detects changes to a "draft state" and produces a brand new
      // immutable state based off those changes
      state.key = action.payload
    },
    change_pw: (state, action) => {
      state.key = action.payload
    },
    logout: state => {
      state.key = null
    }
  }
})

// Action creators are generated for each case reducer function
export const { login, change_pw, logout } = authSlice.actions

export default authSlice.reducer
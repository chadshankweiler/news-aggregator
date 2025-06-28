"use client"

import { configureStore, combineReducers } from '@reduxjs/toolkit';
import keplerGlReducer from '@kepler.gl/reducers';

const rootReducer = combineReducers({
  keplerGl: keplerGlReducer,
});

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) => getDefaultMiddleware({
     serializableCheck: false,
     immutableCheck: false,
  }),
});

export type RootState = ReturnType<typeof rootReducer>;
export type AppDispatch = typeof store.dispatch;
export default store;

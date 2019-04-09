import {createStore, combineReducers, applyMiddleware } from 'redux';
import { Reducer, initialState } from './reducer';
import { Networks } from "./networks";
import { Pictures } from "./pictures";
import thunk from 'redux-thunk';
import logger from 'redux-logger';

export const ConfigureStore = () => {
    const store = createStore(
        combineReducers({
            pictures: Pictures,
            networks: Networks
        }),
        applyMiddleware(thunk, logger)
    );

    return store;
};
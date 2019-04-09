import * as ActionTypes from "./ActionTypes";

export const Networks = (state  = { isLoading: true,
    errMess: null,
    networks:[]}, action) => {
    switch (action.type) {
        case ActionTypes.ADD_NETWORKS:
            return {...state, isLoading: false, errMess: null, networks: action.payload};

        case ActionTypes.NETWORKS_LOADING:
            return {...state, isLoading: true, errMess: null, networks: []};

        case ActionTypes.NETWORKS_FAILED:
            return {...state, isLoading: false, errMess: action.payload};

        default:
            return state;
    }
};
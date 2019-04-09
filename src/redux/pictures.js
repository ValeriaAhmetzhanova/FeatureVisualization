import * as ActionTypes from './ActionTypes';

export const Pictures = (state  = { isLoading: true,
    errMess: null,
    pictures:[]}, action) => {
    switch (action.type) {
        case ActionTypes.ADD_PICTURES:
            return {...state, isLoading: false, errMess: null, pictures: action.payload};

        case ActionTypes.PICTURES_LOADING:
            return {...state, isLoading: true, errMess: null, pictures: []};

        case ActionTypes.PICTURES_FAILED:
            return {...state, isLoading: false, errMess: action.payload};

        default:
            return state;
    }
};
import { NETWORKS } from "../shared/networks";
import { PICTURES } from "../shared/pictures";

export const initialState = {
    networks: NETWORKS,
    pictures: PICTURES
};

export const Reducer = (state = initialState, action) => {
    return state;
};
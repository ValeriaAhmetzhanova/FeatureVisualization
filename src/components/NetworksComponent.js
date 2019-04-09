import React, { Component } from 'react';
import { baseUrl } from '../shared/baseUrl';

import {
    Card, CardBody,
    CardTitle, Media, Button
} from 'reactstrap';

class Networks extends Component {

    constructor(props) {
        super(props);

        this.state = {
            selectedNetwork: null
        }
    }

    onNetworkSelect(network) {
        this.setState({ selectedNetwork: network});
        console.log(network);
    }

    static renderNetwork(network) {
        if (network != null)
            return(
                <Media body className="ml-5 m-2">
                    <Media heading>Selected network is {network.name}</Media>
                    <p>{network.description}</p>
                </Media>
            );
        else
            return(
                <div></div>
            );
    }

    render() {
        const networks = Object.values(this.props.networks.networks).map((network) => {
            return (
                <div className="col-12 col-md-5 m-1">
                    <Card key={network.id}
                          onClick={() => this.onNetworkSelect(network)}>
                        <CardBody>
                            <CardTitle>{network.name}</CardTitle>
                        </CardBody>
                    </Card>
                </div>
            );
        });

        return (
            <div className="container">
                <div className="row">
                <div className="col-12 col-md-5 m-1">
                    {networks}
                </div>
                    <div  className="col-12 col-md-5 m-1">
                        {Networks.renderNetwork(this.state.selectedNetwork)}
                    </div>
                </div>
                <Button type="submit" >
                    Go!
                </Button>
            </div>
        );
    }

}

export default Networks;
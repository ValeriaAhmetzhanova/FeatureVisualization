import React, { Component } from 'react';
import { Media } from 'reactstrap';
import { baseUrl } from '../shared/baseUrl';

class Gallery extends Component {

    render() {
        const gallery = this.props.pictures.pictures.map((picture) => {
            return(
                <div key={picture.id} className="col-12 mt-5">
                    <Media tag="li">
                        <Media left middle>
                            <Media object src={picture.image} alt={picture.name} />
                        </Media>
                        <Media body className="ml-5">
                            <Media heading>{picture.name}</Media>
                            <p>{picture.description}</p>
                        </Media>
                    </Media>
                </div>
            );
        });

        return (
            <div className="container">
                <div className="row">
                    <Media list>
                        {gallery}
                    </Media>
                </div>
            </div>
        );
    }
}

export default Gallery;
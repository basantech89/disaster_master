import React from 'react';
import { Media, Breadcrumb, BreadcrumbItem, Button } from 'reactstrap';
import { Link } from 'react-router-dom';
import { baseUrl } from '../shared/baseUrl';
import { Loading } from './LoadingComponent';

function RenderMenuItem({favorite, deleteFavorite}) {
    const dish = favorite.dishes;
    return(
        <Media tag="li">
            <Media left middle>
                <Media object src={baseUrl + dish.image} alt={dish.name} />
            </Media>
            <Media body className="ml-5">
                <Media heading> {dish.name} </Media>
                <p> {dish.description} </p>
                <Button outline color="danger" onClick={() => deleteFavorite(favorite.id)}>
                    <span className="fa fa-times"/>
                </Button>
            </Media>
        </Media>
    );
}

// functional component
const Favorites = (props) => {
    if (props.favorites.isLoading) {
        return(
            <div className="container">
                <div className="row">
                    <Loading/>
                </div>
            </div>
        );
    }
    else if (props.favorites.errMess) {
        return(
            <div className="container">
                <div className="row">
                    <h4> {props.favorites.errMess} </h4>
                </div>
            </div>
        );
    }
    else if (props.favorites.favorites) {
        const favorites = props.favorites.favorites.map((favorite) => {
            return(
                <div key={favorite.dishes.id} className="col-12 mt-5">
                    <RenderMenuItem favorite={favorite} deleteFavorite={props.deleteFavorite} />
                </div>
            );
        });
        return(
            <div className="container">
                <div className="row">
                    <Breadcrumb>
                        <BreadcrumbItem><Link to='/home'> Home </Link></BreadcrumbItem>
                        <BreadcrumbItem active> My Favorites </BreadcrumbItem>
                    </Breadcrumb>
                    <div className="col-12">
                        <h3> My Favorites </h3>
                        <hr/>
                    </div>
                </div>
                <div className="row">
                    <Media list>
                        {favorites}
                    </Media>
                </div>
            </div>
        );
    }
    else {
        return(
            <div className="container">
                <div className="row">
                    <h4> You have no favorites </h4>
                </div>
            </div>
        );
    }
};

export default Favorites;
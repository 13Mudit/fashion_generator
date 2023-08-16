import { useState } from "react";

function Product(props){
    return (
        <div> 
            <p>Hey this is a new product! {props.image} , {props.description} </p>
        </div>
    );
}

export default Product;
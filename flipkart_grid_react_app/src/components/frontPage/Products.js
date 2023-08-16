// import {ProductsList} from './SearchBar/SearchBar.js';
import {useState} from 'react';
import { Start } from './SearchBar/SearchBar';

import React from 'react';

const ProductComponent = ({ image, flipkartLink }) => {
  return (
    <div>
      
      <a href = {flipkartLink} target = "_blank"> <img src ={image}/> </a>
      <br />
    </div>
  );
};


const Products = ({ ProductsList }) => {
//   console.log("ProducstList size", ProductsList.length);
  
    try{
        return (
            <div>
            <h2>Products List</h2>
            {ProductsList.map(product => (
                <ProductComponent image={product.image_url} flipkartLink={product.url} />
            ))}
            </div>
        );
    } catch {
        return <p> Sorry no similar products available </p>
    }
};
  
export default Products;

// import {ProductsList} from './SearchBar/SearchBar.js';
import {useState} from 'react';
import { Start } from './SearchBar/SearchBar';

import React from 'react';

const ProductComponent = ({ id, name }) => {
  return (
    <div>
      <h3>Product ID: {id}</h3>
      <p>Product Name: {name}</p>
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
                <ProductComponent key={product.id} id={product.id} name={product.name} />
            ))}
            </div>
        );
    } catch {
        return <p> Sorry no similar products available </p>
    }
};
  
export default Products;

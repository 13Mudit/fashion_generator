// import {ProductsList} from './SearchBar/SearchBar.js';
import {useState} from 'react';
import { ProductsList, Start } from './SearchBar/SearchBar';

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
  
  const [msg, setMsg] = useState();
  
    if(Start === 1){
        <p>What are looking today</p>
    }
    else{
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
    }
  
};

export default Products;

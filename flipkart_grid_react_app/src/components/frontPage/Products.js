// import {ProductsList} from './SearchBar/SearchBar.js';
import {useState} from 'react';
import { ProductsList } from './SearchBar/SearchBar';

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
  const [msg, setMsg] = useState('No similar items available');
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
    return <p> {msg} </p>
  }
};

export default Products;

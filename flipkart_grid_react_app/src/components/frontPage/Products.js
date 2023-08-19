// import {ProductsList} from './SearchBar/SearchBar.js';
import {useState} from 'react';
import { Start } from './SearchBar/SearchBar';
import './Product.css';
import React from 'react';

const ProductComponent = ({ image, flipkartLink }) => {
  return (
    <div className='article-card'>
      
      <a href = {flipkartLink} target = "_blank"> <img src ={image} className='image-cls'/> </a>
      <br />
      <br />
    </div>
  );
};


const Products = ({ ProductsList }) => {
//   console.log("ProducstList size", ProductsList.length);
  
    try{
        return (
            <div>
            <h2 className='product-head'>Products List</h2>
            <div className='product-head-border'></div>
            <div className='product-head-border2'></div>
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

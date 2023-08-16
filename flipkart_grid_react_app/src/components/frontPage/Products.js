import {useState} from 'react';
import Product from './Product';
function Products(){
    return (
        <div> 
            <Product image = 'img1' description = 'desc1' />
            <Product image = 'img2' description = 'desc2' />

        </div>
    )
}
export default Products;
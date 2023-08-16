import './App.css';
import SearchBar from './components/frontPage/SearchBar/SearchBar.js';
import Products from "./components/frontPage/Products.js";

function App() {
  return (
    <div className="App">
      <div className = "left">
        <SearchBar/>
      </div>
      <div className = "right">
        <Products />
      </div>
    </div>
  );
}

export default App;

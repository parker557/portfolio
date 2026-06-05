import * as React from 'react';
import HomePage from './screens/HomePage.js';
import FeaturesPage from './screens/FeaturesPage.js';
import PurchasePage from './screens/PurchasePage.js';
import ContactPage from './screens/ContactPage.js';
import PaymentPage from './screens/PaymentPage.js';
import Navbar from './components/NavBar/NavBar.js';
import Footer from './components/Footer/Footer.js';
import {Route, Routes} from 'react-router-dom'

function App() {
  return (
    <>
      <Navbar/>
        <Routes>
          <Route path="/" element={<HomePage/>}></Route>
          <Route path="/features" element={<FeaturesPage/>}></Route>
          <Route path="/purchase" element={<PurchasePage/>}></Route>
          <Route path="/contact" element={<ContactPage/>}></Route>

          <Route path="/payment" element={<PaymentPage/>}></Route>
        </Routes>
      <Footer/>
    </>
  );
}

export default App;

import * as React from 'react';
import { useState, useEffect } from 'react';
import './css/PaymentPage.css'

// import { Elements, useStripe, useElements, PaymentElement } from '@stripe/react-stripe-js';
// import { loadStripe } from '@stripe/stripe-js';


function PaymentPage() {

  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);


  const handlePayment = () => {
    alert("Successful! Thank you")
  };


  const [plan, setPlan] = useState(urlParams.get('plan')==1?"Start Up Plan":"Bussiness Plan")
  const [subscription, setSubpscription] = useState(urlParams.get('length') ==1? "Monthly" : "Yearly")
  const [method, setMethod] = useState({ infoMsg: "" });

  const [price,setPrice] = useState(getPrice())

  function getPrice(){
    if (urlParams.get('plan') == 1) {
      return urlParams.get('length')==1? 1500 : 14400
    }
    else {
      return urlParams.get('length')==1? 5000 : 42000
    }
  }

  function handleRadio(event) {
    var msg;
    if (event.target.value === "Bank") {
      msg = "HSBC Bank Account: RentConnect | Account number: 111-123456-111"
    } else if (event.target.value === "Paypal") {
      msg = "Paypal"
    } else if (event.target.value === "Alipay") {
      msg = "Alipay"
    } else {
      msg = ""
    }

    setMethod(method => ({ infoMsg: msg }));
  }


  return (
    // <Elements stripe={stripePromise} options={options}>
      <section id='payment'>
        <div className='payment-container'>
          <h1>1. Confirm plan</h1>
          <hr />
          <div className='itemContainer'>
            <h2>{plan}</h2>
            <h3>{subscription}</h3>
            <h3> HKD$ {price}</h3>
          </div>
          <hr className='break' />
          <form action="/" required>
            <h1>2. Fill in your information</h1>
            <hr />
            <div className='userInfoContainer'>
              <div className='grid-item'>
                <label for='fname'>First name:</label>
                <input type='text' id='fname' placeholder='Required' required></input>
              </div>
              <div className='grid-item'>
                <label for='lname'>Last name:</label>
                <input type='text' id='lname' placeholder='Required' required></input>
              </div>
              <div className='grid-item'>
                <label for='email'>Email address:</label>
                <input type='text' id='email' placeholder='Required' required></input>
              </div>
              <div className='grid-item'>
                <label for='phone'>Phone number:</label>
                <input type='text' id='phone' placeholder='Required' required></input>
              </div>
              <div className='grid-item'>
                <label for='company'>Company name:</label>
                <input type='text' id='company' placeholder='Optional'></input>
              </div>
              <div className='grid-item'>
                <label for='remark'>Remark:</label>
                <textarea id='remark' rows="5" cols="50" placeholder='Optional'></textarea>
              </div>
            </div>
            <hr className='break' />


            <h1>3. Choose payment methods</h1>
            <hr />
            <div className='methodContainer'>

              <div className='options-group'>
                <h3>Methods</h3>
                <div className='option'>
                  <input type='radio' id='Bank' name='methods' value='Bank' defaultChecked onClick={handleRadio}></input>
                  <label for='Bank'>Bank transfer</label>
                </div>
                <div className='option'>
                  <input type='radio' id='Paypal' name='methods' value='Paypal' onClick={handleRadio}></input>
                  <label for='Paypal'>PayPal</label>
                </div>
                <div className='option'>
                  <input type='radio' id='AilPay' name='methods' value='Alipay' onClick={handleRadio}></input>
                  <label for='AilPay'>AliPay</label>
                </div>
              </div>

              <div className='methodInfo'>
                <h3>Information</h3>
                <p className='methodInfoText'>{method.infoMsg}</p>
              </div>
            </div>
            <hr className='break' />

            <h1>4. Pay</h1>
            <hr />
            <div className='itemContainer'>
              <p>Total Price: HKD${price}</p>
            </div>
            <button className='submitButton' type='submit' onClick={() => handlePayment()}>Confirm and pay</button>
          </form>

        </div>
      </section>
    // </Elements>
  );
}

export default PaymentPage;
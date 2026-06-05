import * as React from 'react';
import Button from '@mui/material/Button';
import './css/PurchasePage.css'


function PurchasePage() {
    return (
        <div id='container'>

            <h1 class="textbox"> Price Plans </h1>
            <div class="pricing-table">
                <div class="plan">
                    <h2>Start Up Plan</h2>
                    <p class="price">$1500/month</p>
                    <p class="price-annual">$14400/year (20% off)</p>
                    <ul class="planContent">
                        <li>Basic Functionality of Rentconnect</li>
                        <li>Maintenance</li>
                        <li>1000 property listing</li>
                        <li>Contract management</li>
                        <li>Monthly Report on listing</li>
                        <li>Online Customer Support</li>
                    </ul>
                    <Button class="select-plan" href="/payment?plan=1&length=1">Select Monthly Plan</Button>
                    <Button class="select-plan" href="/payment?plan=1&length=2">Select Yearly Plan</Button>

                </div>
                <div class="plan">
                    <h2>Business Plan</h2>
                    <p class="price">$5000/month</p>
                    <p class="price-annual">$42000/year (30% off)</p>
                    <ul class="planContent">
                        <li>Everything in Basic Plan</li>
                        <li>10000 property listing</li>
                        <li>Customization</li>
                        <li>Monthly Report on User Activity and User Engagement</li>
                        <li>Highlight Most Engaged Listing</li>
                        <li>Reports and Analytics</li>
                        <li>Marketing Template</li>
                        <li>Training and Customer Support</li>
                    </ul>
                    <Button class="select-plan" href="/payment?plan=2&length=1">Select Monthly Plan</Button>
                    <Button class="select-plan" href="/payment?plan=2&length=2">Select Yearly Plan</Button>

                </div>
                <div class="plan">
                    <h2>Enterprise Plan</h2>
                    <p>Contact Customer Service for presentation</p>
                    <Button  class="contact-sales" href="/contact"> Contact Sales </Button>
                </div>
            </div>

        </div>
    )
}

export default PurchasePage;
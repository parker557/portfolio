import * as React from 'react';
import Button from '@mui/material/Button'
import './css/HomePage.css'
import KeyboardIcon from '@mui/icons-material/Keyboard';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import SettingsIcon from '@mui/icons-material/Settings';
import PublicIcon from '@mui/icons-material/Public';
import OndemandVideoIcon from '@mui/icons-material/OndemandVideo';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import AccordionMUI from '../components/Accordion/AccordionMUI';
import Showcase from '../image/HomePage_showcase.png';

function HomePage() {
    return (
        <>
            <section id='introduction'>
                <div id='introInfoContainer'>
                    <div className='textbox'>
                        <h1>Your trading platform creator</h1>
                        <ul>
                            <li>Seeking for a <span>low-cost</span> and <span>efficient</span> workflow?</li>
                            <li>Want to expand your business on a <span>global scale</span>?</li>
                            <li>Want to <span>differentiate yourself</span> from other competitors?</li>
                        </ul>
                        <p>RentConnect creates a tailor-made SaaS trading platform with high 
                            customization for you. All you need to do is chatting with our consultants,
                            and our development team will bring your idea in reality!
                        </p>
                        <Button href="/features" variant='contained' sx={{mr: 2, mt: 3}}>Learn more</Button>
                        <Button href="/purchase" variant='contained' sx={{mt: 3}}>Start Now</Button>
                    </div>
                    <img src={Showcase} alt="product"></img>
                </div>

            </section>
    
            <section id='features'>
                <div id='basicContainer'>
                    <h1>Basic functions</h1>
                    <p>A set of basic functionalities for the trading platform will
                        be included in any subscription plan.
                    </p>
                    <h3>Key functions</h3>
                    <ul>
                        <li>Database (medium size)</li>
                        <li>Login system</li>
                        <li>Listing system</li>
                        <li>Searching system</li>
                        <li>Comparsion system</li>
                        <li>End-to-End chatroom</li>
                        <li>Payment system</li>
                    </ul>
                </div>
                <div id='extraContainer'>
                    <h1>Additional features</h1>
                    <p>A set of additional features for the trading platform add
                        some favors in your trading platform. Higher subscription
                        plan will include more features.
                    </p>
                    <h3>Key functions</h3>
                    <ul>
                        <li>Database (up to unlimited)</li>
                        <li>User analysis system</li>
                        <li>Pair rental system</li>
                        <li>Advanced searching system</li>
                        <li>Recommendation algorithm</li>
                        <li>Document management system</li>
                        <li>Dynamic pricing system</li>
                        <li>AI customer support</li>
                        <p className='fullstop'>......</p>
                    </ul>
                </div>
            </section>

            <section id='advantages'>
                <h1>Advantages of digital trading platform</h1>
                <div className='boxSet'>
                    <div className='box'>
                        <p>Reduce for manual data entry</p>
                        <KeyboardIcon/>
                    </div>
                    <div className='box'>
                        <p>Saves your data in cloud</p>
                        <CloudUploadIcon/>
                    </div>
                    <div className='box'>
                        <p>Perform analysis automatically</p>
                        <SettingsIcon/>
                    </div>
                    <div className='box'>
                        <p>Expand your business without boundary</p>
                        <PublicIcon/>
                    </div>
                    <div className='box'>
                        <p>Demonstrate your product with multimedia</p>
                        <OndemandVideoIcon/>
                    </div>
                    <div className='box'>
                        <p>Differentiate yourself with unique features</p>
                        <EmojiEventsIcon/>
                    </div>
                </div>
            </section>

            <section id='QA'>
                <h1>Q & A</h1>
                <div className='AccordionList'>
                    <AccordionMUI question="What does RentConnect offer?" 
                    answer="RentConnect is a property-specific SaaS vendor that tailor-made
                    SaaS-based trading platforms for property retail agencies. It runs a 
                    website(You are here!) for showcasing possible features and consulting services."/>
                    <AccordionMUI question="Who should use RentConnect?" 
                    answer="As long as you are working in the property industry and you want to increase your tenant pool, 
                    get a competitive advantage on the market and be eager to reduce costs in your business. 
                    You are our perfect customer."/>
                    <AccordionMUI question="What is SaaS?" 
                    answer="Software as a service (SaaS) is a software distribution model. 
                    The software provider (RentConnect) will host the application and related data for the user,
                     and the user simply pays a subscription fee to gain access to the software 
                     via any device that connects to the network without worrying about the setup and maintenance of the software. "/>
                </div>
            </section>
        </>
    )
}

export default HomePage;
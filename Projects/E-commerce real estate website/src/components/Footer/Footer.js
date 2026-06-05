import React from "react";
import classes from './Footer.module.css'
import GoogleIcon from '@mui/icons-material/Google';
import FacebookIcon from '@mui/icons-material/Facebook';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import icon from "../../image/RentConnect_Logo.jpg"

function Footer() {
    return (
        <>
            <div className={classes.desktop}>
                <section className={classes.footer}>
                    <div className={classes.container}>
                        <div className={classes.brandContainer}>
                            <img src={icon} alt="icon"></img>
                            <div className={classes.brandSet}>
                                <div className={classes.brand}>RentConnect</div>
                                <div className={classes.slogan}>Connecting Homes, Building Relationships</div>
                            </div>
                        </div>

                        <p>
                            We are a team of university undergraduates focused on providing technical solutions for the property industry.
                            We hold an official website that provides consulting services for our customers and showcases some possible 
                            features of a property trading platform. Let us know your needs and we will create a tailor-made trading platform for you.
                        </p>
                    </div>
                    <div className={classes.container}>
                        <h1>Contact Us</h1>
                        <p>TEL: +1 7064096605   +852 54896264</p>
                        <p>TEL: services@rentconnect.org</p>
                        <p>Discord: <a className={classes.link} href="https://discord.gg/VjBTHQ7bp2">https://discord.gg/VjBTHQ7bp2</a></p>
                    </div>
                    <div className={classes.container}>
                        <h1>Follow Us</h1>
                        <div className={classes.buttonSet}>
                            <GoogleIcon sx={{mr: 1}}/>
                            <FacebookIcon sx={{mx: 1}}/>
                            <LinkedInIcon sx={{ml: 1}}/>
                        </div>
                    </div>
                </section>
            </div>
            <div className={classes.mobile}>
                <section className={classes.footer}>
                    <div className={classes.container}>
                        <div className={classes.brandContainer}>
                            <img src="https://via.placeholder.com/40" alt="icon"></img>
                            <div className={classes.brandSet}>
                                <div className={classes.brand}>RentConnect</div>
                                <div className={classes.slogan}>Connecting Homes, Building Relationships</div>
                            </div>
                            <div className={classes.container}>
                                <h1>Contact Us</h1>
                                <p>TEL: +1 7064096605   +852 54896264</p>
                                <p>TEL: services@rentconnect.org</p>
                                <p>Discord: <a className={classes.link} href="https://discord.gg/VjBTHQ7bp2">https://discord.gg/VjBTHQ7bp2</a></p>
                            </div>
                            <div className={classes.container}>
                                <h1>Follow Us</h1>
                                <div className={classes.buttonSet}>
                                    <GoogleIcon sx={{mr: 1}}/>
                                    <FacebookIcon sx={{mx: 1}}/>
                                    <LinkedInIcon sx={{ml: 1}}/>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </>
    )
}

export default Footer;
import React from "react";
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import './css/ContactPage.css';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';

function ContactPage() {
    const handleSubmit = (event) => {
        event.preventDefault();
    
        const confirmed = window.confirm("Are you sure you want to submit?");
        
        if (confirmed) {
            window.location.href = "http://localhost:3000/";
        }
    };

    return (
        <>
            <section id="intro" className="intro-section">
                <Container maxWidth="lg">
                    <Grid container spacing={3}>
                        <Grid item xs={12} md={6}>
                            <div className="intro-content">
                                <h1 className="intro-heading">Contact Us</h1>
                                <p className="intro-text">Have questions or need assistance? Feel free to reach out to us.</p>
                                <Button href="/contact" variant='contained' size="large">Contact Us</Button>
                            </div>
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <div className="contact-image">
                                {/* 这里可以添加联系方式图片 */}
                            </div>
                        </Grid>
                    </Grid>
                </Container>
            </section>
            <section id="contact-form" className="contact-section">
                <Container maxWidth="md">
                    <h2 className="contact-heading">Send us a message</h2>
                    <form onSubmit={handleSubmit} className="contact-form">
                        <Grid container spacing={3}>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    required
                                    id="firstName"
                                    name="firstName"
                                    label="First name"
                                    fullWidth
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    required
                                    id="lastName"
                                    name="lastName"
                                    label="Last name"
                                    fullWidth
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    id="email"
                                    name="email"
                                    label="Email"
                                    fullWidth
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    id="message"
                                    name="message"
                                    label="Message"
                                    multiline
                                    rows={4}
                                    fullWidth
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <Button type="submit" variant="contained" color="primary">
                                    Send Message
                                </Button>
                            </Grid>
                        </Grid>
                    </form>
                </Container>
            </section>
        </>
    );
}

export default ContactPage;

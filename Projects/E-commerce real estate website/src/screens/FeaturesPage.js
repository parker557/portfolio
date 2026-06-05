import React from "react";
import Button from '@mui/material/Button'
import './css/FeaturesPage.css'
import CardMUI from "../components/Card/CardMUI";
import Data from '../CardData.json'
import Container from '@mui/material/Container'
import Grid from '@mui/material/Grid'

function FeaturesPage() {
    return (
        <>
            <section id="intro">
                <h1>Discover possible features for your trading platform</h1>
                <div className="buttonSet">
                    <p>Didn't found what you want? Talk to us, let us create it for you.</p>
                    <Button href="/contact" variant='contained' size="small" sx={{ml: 2}}>Consulting service</Button>
                </div>
            </section>
            <section id="content">
                <Container maxWidth="lg">
                    <Grid container spacing={5} style={{marginTop: '20px'}}>
                        {Data.map((result)=>(
                            <CardMUI title={result.title} content={result.content} img={result.img}/>
                        ))}
                    </Grid>
                </Container>
            <div className="text"><p>More features will be released soon......</p></div>
            </section>
        </>
    );
}

export default FeaturesPage;
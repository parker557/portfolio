import React from "react";
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid'
import unknown from '../../image/unknown.jpg'
import analysis from '../../image/Analysis.jpg'
import pair from '../../image/PairRental.png'
import search from "../../image/Searching.jpg"
import recommendation from "../../image/Recommendation.jpg"
import pricing from "../../image/Pricing.jpg"
import AI from "../../image/AISupport.jpg"

function CardMUI(props) {
    var image = props.img;
    if (image.includes("Analysis.jpg")) {
        image = analysis
    } else if (image.includes("PairRental.png")) {
        image = pair
    } else if (image.includes("Searching.jpg")) {
        image = search
    } else if (image.includes("Recommendation.jpg")) {
        image = recommendation
    } else if (image.includes("Pricing.jpg")) {
        image = pricing
    } else if (image.includes("AISupport.jpg")) {
        image = AI
    } else {
        image = unknown
    }
    return(
        <>   
            <Grid item xs={12} sm={4} ms={4}>
                <Card sx={{ maxWidth: 345 }} style={{padding: '10px', marginBottom: '30px'}}>
                <CardMedia
                    sx={{ height: 200 }}
                    image={image}
                    title={props.title}
                    style={{borderRadius:'5px'}}
                />
                <CardContent>
                    <Typography gutterBottom variant="h5" component="div">
                    {props.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                    {props.content}
                    </Typography>
                </CardContent>
                <CardActions><Button variant="contained" disabled>View Demo</Button></CardActions>
                </Card>
            </Grid>
        </>
    )
}

export default CardMUI
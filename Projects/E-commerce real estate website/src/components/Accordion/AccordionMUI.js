import * as React from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';

export default function AccordionMUI(props) {
  return (
    <div>
      <Accordion sx={{boxShadow: 2}}>
        <AccordionSummary
          expandIcon={<ArrowDropDownIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
          sx={{}}
        >
          <Typography sx={{fontWeight: 'bold'}}>{props.question}</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>{props.answer}</Typography>
        </AccordionDetails>
      </Accordion>
    </div>
  );
}


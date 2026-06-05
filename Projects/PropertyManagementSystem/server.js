import { OpenAI } from 'openai'; // Corrected import statement for OpenAI
import express from 'express';
import bodyParser from 'body-parser';
import session from 'express-session';
import path from 'path';
import http from 'http'; // Required for Socket.IO
import { Server } from 'socket.io';
import { fileURLToPath } from 'url';


// const OpenAI = require('openai');
// const express = require('express');
// const bodyParser = require('body-parser');
// const session = require('express-session');
// const path = require('path');
// const http = require('http'); // Required for Socket.IO
// const { Server } = require('socket.io');
const openai = new OpenAI({
    baseURL: 'https://api.deepseek.com',
    apiKey: process.env.DEEPSEEK_API_KEY
});

const app = express();
const server = http.createServer(app);
const io = new Server(server);


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(
    session({
        secret: 'property_management_secret',
        resave: false,
        saveUninitialized: true,
    })
);

// Mock data
let properties = [
    { propertyID: 1, buildingNo: 'B1', roomNo: '101', squareMeter: 50, bedrooms: 2 },
    { propertyID: 2, buildingNo: 'B1', roomNo: '102', squareMeter: 60, bedrooms: 3 },
    { propertyID: 3, buildingNo: 'B2', roomNo: '101', squareMeter: 80, bedrooms: 3 },
];

let ownerProperties = [
    { ownerID: 1, propertyID: 1, isRented: true, rentalDate: '2025-01-01', isPurchased: false, purchaseDate: null },
    { ownerID: 1, propertyID: 2, isRented: false, rentalDate: null, isPurchased: true, purchaseDate: '2024-12-01' },
    { ownerID: 3, propertyID: 3, isRented: false, rentalDate: null, isPurchased: true, purchaseDate: '2024-6-01' },
];

let users = [
    { id: 1, role: 'owner', username: 'owner1', password: 'password1' },
    { id: 2, role: 'staff', username: 'staff1', password: 'password2' },
    { id: 3, role: 'owner', username: 'owner2', password: '123' },
    { id: 3, role: 'maintainer', username: 'maintainer1', password: '123' },
    { id: 3, role: 'maintainer', username: 'maintainer2', password: '123' },
];

let repairRequests = [];
let chatMessages = [
    { role: 'staff', sender: 'staff1', text: 'Welcome to the chat!', time: '2025-01-01 10:00:00' },
    { role: 'owner', sender: 'owner1', text: 'Hello, I need assistance with my property.', time: '2025-01-01 10:00:05' },
    { role: 'staff', sender: 'staff1', text: 'Sure, how can I help you today?', time: '2025-01-01 10:00:20' },
];

let noticeMessages = [
    {ownerID: 1, property: 'B1-101', issue: 'You need to pay the property fee.', date: '2025-1-1', time: '15:53:45'}, 
    {ownerID: -1, property: '-', issue: 'Water supply will be cut off on Monday, January 5th for maintenance.', date: '2025-1-1', time: '10:00:45'}
];

// User authentication
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    const user = users.find(u => u.username === username && u.password === password);

    if (user) {
        req.session.user = user;
        res.json({ success: true, role: user.role, id: user.id, username: user.username });
    } else {
        res.status(401).json({ success: false, message: 'Invalid credentials' });
    }
});


app.get('/chat-user-data', (req, res) => {
    if (req.session.user) {
        res.json({
            username: req.session.user.username,
            role: req.session.user.role
        });
    } else {
        res.status(403).json({ message: 'Unauthorized' });
    }
});

// GPT Response Endpoint
app.post('/deepseek-response', async (req, res) => {
    const { role, text } = req.body;

    // const openaiRole = role === 'staff' ? 'assistant' : 'user';

    try {
        const completion = await openai.chat.completions.create({
            messages: [{ role: "system", content: text }],
            model: "deepseek-chat",
        });

        const responseMessage = completion.choices[0].message.content;
        res.json({ response: responseMessage });
    } catch (error) {
        console.error("Error calling OpenAI API:", error);
        res.status(500).json({ error: "Failed to fetch DeepSeek response" });
    }
});


// Owner routes
app.get('/owner/properties', (req, res) => {
    if (req.session.user && req.session.user.role === 'owner') {
        const ownerID = req.session.user.id;
        const ownedProperties = ownerProperties
            .filter(op => op.ownerID === ownerID)
            .map(op => {
                const propertyDetails = properties.find(p => p.propertyID === op.propertyID);
                return { ...op, ...propertyDetails };
            });
        res.json({ properties: ownedProperties });
    } else {
        res.status(403).json({ message: 'Unauthorized' });
    }
});

app.get('/staff/properties', (req, res) => {
    if (req.session.user && req.session.user.role === 'staff') {
        const allProperties = ownerProperties.map(op => {
            const propertyDetails = properties.find(p => p.propertyID === op.propertyID);
            return { ...op, ...propertyDetails };
        });
        // console.log(allProperties);
        res.json({ properties: allProperties });
    } else {
        res.status(403).json({ message: 'Unauthorized' });
    }
});


const getMaintainer = () => {
    const maintainers = users.filter(user => user.role === 'maintainer');
    if (maintainers.length === 0) {
        return '-';
    }
    const randomIndex = Math.floor(Math.random() * maintainers.length);
    return maintainers[randomIndex].username;
};



app.post('/owner/repair', (req, res) => {
    if (req.session.user && req.session.user.role === 'owner') {
        const { propertyID,buildingNo,roomNo, issue } = req.body;

        if (!propertyID || !buildingNo || !roomNo || !issue.trim()) {
            return res.status(400).json({ success: false, message: 'Invalid data. Please provide all required fields.' });
        }

        const currentDate = new Date();
        const date = currentDate.toISOString().split('T')[0]; // YYYY-MM-DD
        const time = currentDate.toTimeString().split(' ')[0]; // HH:MM:SS
        const assignedMaintainer = getMaintainer();

        repairRequests.push({
            id: repairRequests.length + 1,
            ownerID: req.session.user.id,
            property: `${buildingNo}-${roomNo}`,
            issue,
            status: 'Pending',
            maintainer: assignedMaintainer,
            date,
            time,
        });
        res.json({ success: true, message: 'Repair request submitted' });
    } else {
        res.status(403).json({ success: false, message: 'Unauthorized' });
    }
});

app.post('/staff/notice', (req, res) => {
    if (req.session.user && req.session.user.role === 'staff') {
        const { ownerID,buildingNo,roomNo, issue } = req.body;

        if (!issue.trim()) {
            return res.status(400).json({ success: false, message: 'Invalid data. Please provide all required fields.' });
        }

        const currentDate = new Date();
        const date = currentDate.toISOString().split('T')[0]; // YYYY-MM-DD
        const time = currentDate.toTimeString().split(' ')[0]; // HH:MM:SS

        noticeMessages.push({
            // id: noticeMessages.length + 1,
            ownerID,
            property: `${buildingNo}-${roomNo}`,
            issue,
            date,
            time,
        });

        // console.log(noticeMessages);
        res.json({ success: true, message: 'Notice submitted' });
    } else {
        res.status(403).json({ success: false, message: 'Unauthorized' });
    }
});

app.post('/owner/chat', (req, res) => {
    if (req.session.user && req.session.user.role === 'owner') {
        const { message } = req.body;
        const newMessage = {
            id: chatMessages.length + 1,
            sender: 'owner',
            message,
            timestamp: new Date().toISOString(),
        };
        chatMessages.push(newMessage);
        res.json({ success: true, message: 'Message sent' });
    } else {
        res.status(403).json({ message: 'Unauthorized' });
    }
});

// Staff routes
app.get('/staff/repairs', (req, res) => {
    if (req.session.user && req.session.user.role === 'staff') {
        const detailedRepairs = repairRequests.map(req => {
            const propertyDetails = properties.find(p => p.propertyID === req.propertyID);
            return { ...req, ...propertyDetails };
        });
        res.json(detailedRepairs);
    } else {
        res.status(403).json({ message: 'Unauthorized' });
    }
});


app.get('/owner/notice', (req, res) => {
    if (req.session.user && req.session.user.role === 'owner') {
        const id = req.session.user.id;
        // console.log('id: ' + id);
        const detailedNotices = noticeMessages.filter(nm => nm.ownerID === id);
        
        // console.log('detailedNotices: ');
        // console.log(detailedNotices);
        res.json(detailedNotices);
    } else {
        res.status(403).json({ message: 'Unauthorized' });
    }
});


app.get('/owner/public-notice', (req, res) => {
    if (req.session.user && req.session.user.role === 'owner') {
        const id = -1;

        const detailedNotices = noticeMessages.filter(nm => nm.ownerID === id);
    
        res.json(detailedNotices);
    } else {
        res.status(403).json({ message: 'Unauthorized' });
    }
});


app.post('/staff/repair/update', (req, res) => {
    if (req.session.user && req.session.user.role === 'staff') {
        const { id, status } = req.body;
        const request = repairRequests.find(r => r.id === id);
        if (request) {
            request.status = status;
            res.json({ success: true, message: 'Repair request updated' });
        } else {
            res.status(404).json({ message: 'Request not found' });
        }
    } else {
        res.status(403).json({ message: 'Unauthorized' });
    }
});

app.get('/staff/payments', (req, res) => {
    if (req.session.user && req.session.user.role === 'staff') {
        const payments = [
            { paymentID: 'PMT001', date: '2024-01-10', amount: 500, paid: true },
            { paymentID: 'PMT002', date: '2024-02-05', amount: 450, paid: false },
        ];
        res.json(payments);
    } else {
        res.status(403).json({ message: 'Unauthorized' });
    }
});

app.get('/staff/chat', (req, res) => {
    if (req.session.user && req.session.user.role === 'staff') {
        res.json(chatMessages);
    } else {
        res.status(403).json({ message: 'Unauthorized' });
    }
});


// Owner dashboard
app.get('/owner/dashboard', (req, res) => {
    if (req.session.user && req.session.user.role === 'owner') {
        // Retrieve owner-related properties and render the dashboard
        // const ownerID = req.session.user.id;
        // const ownedProperties = ownerProperties
        //     .filter(op => op.ownerID === ownerID)
        //     .map(op => {
        //         const propertyDetails = properties.find(p => p.propertyID === op.propertyID);
        //         return { ...op, ...propertyDetails };
        //     });
        res.sendFile(path.join(__dirname, 'public', 'owner-dashboard.html'));
    } else {
        res.status(403).json({ message: 'Unauthorized access' });
    }
});

// Staff dashboard (can add later if needed)
app.get('/staff/dashboard', (req, res) => {
    if (req.session.user && req.session.user.role === 'staff') {
        res.sendFile(path.join(__dirname, 'public', 'staff-dashboard.html'));
    } else {
        res.status(403).json({ message: 'Unauthorized access' });
    }
});

app.get('/maintainer/dashboard', (req, res) => {
    if (req.session.user && req.session.user.role === 'maintainer') {
        res.sendFile(path.join(__dirname, 'public', 'maintainer-dashboard.html'));
    } else {
        res.status(403).json({ message: 'Unauthorized access' });
    }
});


// WebSocket communication
io.on('connection', (socket) => {
    console.log('A user connected');

    // console.log('Sending chat history:', chatMessages);

    // Send chat history to newly connected client
    socket.emit('chat history', chatMessages);

    // Handle incoming messages
    socket.on('send message', (message) => {
        chatMessages.push(message); // Save message
        io.emit('receive message', message); // Broadcast to all clients
    });

    socket.on('disconnect', () => {
        console.log('A user disconnected');
    });
});


// Serve index.html for login page
// app.get('/', (req, res) => {
//     res.sendFile(path.join(__dirname, 'public', 'index.html'));
// });

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Serve static files (frontend)
app.use(express.static(path.join(__dirname, 'public')));

// Start server
server.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});

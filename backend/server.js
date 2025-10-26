const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const axios = require('axios'); // We need axios to call our Python API
const Complaint = require('./Complaint'); // Import our model

const app = express();

// --- Middleware ---
app.use(cors()); // Allow cross-origin requests (from React)
app.use(express.json()); // Allow our app to accept JSON

// --- Configuration ---
const PORT = 5001; // Port for this Node.js server
const MONGO_URI = "mongodb://127.0.0.1:27017/complaint_system"; // Your local MongoDB
const PYTHON_API_URL = "http://127.0.0.1:5000/predict"; // The URL of your running Python API

// --- Connect to MongoDB ---
mongoose.connect(MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
.then(() => console.log("MongoDB connected successfully."))
.catch(err => console.error("MongoDB connection error:", err));

// ===============================================
// --- API ENDPOINTS ---
// ===============================================

/**
 * @route   POST /api/complaints
 * @desc    Receive a new complaint, get AI prediction, and save to DB
 */
app.post('/api/complaints', async (req, res) => {
    try {
        const { text } = req.body;

        if (!text) {
            return res.status(400).json({ msg: "Complaint text is required." });
        }

        // --- 1. Call the Python AI API ---
        console.log("Sending to Python API:", text);
        const aiResponse = await axios.post(PYTHON_API_URL, {
            text: text
        });

        const { category, priority } = aiResponse.data;
        console.log("Received from Python API:", aiResponse.data);

        // --- 2. Create a new complaint object ---
        const newComplaint = new Complaint({
            text: text,
            category: category,  // From AI
            priority: priority   // From AI
        });

        // --- 3. Save to MongoDB ---
        const savedComplaint = await newComplaint.save();
        
        res.status(201).json(savedComplaint); // Send the full complaint back to React

    } catch (err) {
        console.error("Error in /api/complaints:", err.message);
        res.status(500).send("Server Error");
    }
});


/**
 * @route   GET /api/complaints
 * @desc    Get all complaints for the admin dashboard
 */
app.get('/api/complaints', async (req, res) => {
    try {
        // Find all complaints, sort them by priority (Urgent first)
        // We use a custom sort order for your priorities
        const complaints = await Complaint.find();

        const priorityOrder = { 'Urgent': 1, 'Medium': 2, 'Low': 3 };

        complaints.sort((a, b) => {
            return priorityOrder[a.priority] - priorityOrder[b.priority];
        });

        res.json(complaints);
    } catch (err) {
        console.error("Error in GET /api/complaints:", err.message);
        res.status(500).send("Server Error");
    }
});

/**
 * @route   PUT /api/complaints/:id
 * @desc    Update the status of a complaint
 */
app.put('/api/complaints/:id', async (req, res) => {
    try {
        const { status } = req.body;
        const complaintId = req.params.id;

        if (!status || !['New', 'In-Progress', 'Resolved'].includes(status)) {
            return res.status(400).json({ msg: "Invalid status." });
        }

        const updatedComplaint = await Complaint.findByIdAndUpdate(
            complaintId,
            { status: status },
            { new: true } // Return the updated document
        );

        if (!updatedComplaint) {
            return res.status(404).json({ msg: "Complaint not found." });
        }

        res.json(updatedComplaint);

    } catch (err) {
        console.error("Error in PUT /api/complaints/:id:", err.message);
        res.status(500).send("Server Error");
    }
});


// --- Start The Server ---
app.listen(PORT, () => {
    console.log(`Node.js backend server running on port ${PORT}`);
});
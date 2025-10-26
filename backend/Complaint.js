const mongoose = require('mongoose');

const complaintSchema = new mongoose.Schema({
    text: {
        type: String,
        required: true
    },
    // These two fields will be filled by your AI
    category: {
        type: String,
        required: true,
        enum: ['Roads', 'Water', 'Electricity', 'Waste', 'Other']
    },
    priority: {
        type: String,
        required: true,
        enum: ['Urgent', 'Medium', 'Low']
    },
    // This status will be updated by the admin
    status: {
        type: String,
        enum: ['New', 'In-Progress', 'Resolved'],
        default: 'New'
    },
    submittedAt: {
        type: Date,
        default: Date.now
    }
});

const Complaint = mongoose.model('Complaint', complaintSchema);

module.exports = Complaint;
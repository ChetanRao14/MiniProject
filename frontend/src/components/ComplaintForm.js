import React, { useState } from 'react';
import axios from 'axios';

// We will call this function from App.js to refresh the list
function ComplaintForm({ onComplaintSubmitted }) {
    const [text, setText] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!text) {
            setMessage('Please enter a complaint.');
            return;
        }

        try {
            // Send the complaint to our Node.js backend (running on port 5001)
            const res = await axios.post('http://localhost:5001/api/complaints', { text });
            
            console.log('Complaint submitted:', res.data);
            setMessage('Complaint submitted successfully! Priority: ' + res.data.priority);
            setText(''); // Clear the text box
            
            // Tell the Admin Dashboard to refresh its data
            onComplaintSubmitted(); 

        } catch (err) {
            console.error(err);
            setMessage('Error submitting complaint.');
        }
    };

    return (
        <div className="form-container">
            <h2>Submit a New Complaint</h2>
            <form onSubmit={handleSubmit}>
                <textarea
                    rows="5"
                    placeholder="Describe your issue in detail..."
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                ></textarea>
                <button type="submit">Submit Complaint</button>
            </form>
            {message && <p className="message">{message}</p>}
        </div>
    );
}

export default ComplaintForm;
import React, { useState } from 'react';
import './App.css'; // We will add styles here
import ComplaintForm from './components/ComplaintForm';
import AdminDashboard from './components/AdminDashboard';

function App() {
    // This 'trigger' is a simple trick to connect the two components.
    // When the form is submitted, we'll change this value,
    // which will cause the AdminDashboard to re-fetch its data.
    const [fetchTrigger, setFetchTrigger] = useState(0);

    const handleNewComplaint = () => {
        // Update the trigger to a new value
        setFetchTrigger(prev => prev + 1); 
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>AI Complaint Prioritization System</h1>
                <p>Siddaganga Institute of Technology - AD5</p>
            </header>
            
            <div className="main-content">
                {/* The User Form */}
                <ComplaintForm onComplaintSubmitted={handleNewComplaint} />
                
                {/* The Admin Dashboard */}
                <AdminDashboard fetchTrigger={fetchTrigger} />
            </div>
        </div>
    );
}

export default App;
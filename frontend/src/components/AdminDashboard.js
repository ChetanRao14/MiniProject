import React, { useState, useEffect } from 'react';
import axios from 'axios';

// We pass { fetchTrigger } so the form can tell us to re-fetch
function AdminDashboard({ fetchTrigger }) {
    const [complaints, setComplaints] = useState([]);
    const [loading, setLoading] = useState(true);

    // This function fetches the data from the backend
    const fetchComplaints = async () => {
        setLoading(true);
        try {
            // Get all complaints from our Node.js backend
            const res = await axios.get('http://localhost:5001/api/complaints');
            
            // The backend already sorts them by priority, so we just set them
            setComplaints(res.data);
        } catch (err) {
            console.error("Error fetching complaints:", err);
        }
        setLoading(false);
    };

    // This runs when the component first loads
    // and whenever 'fetchTrigger' changes
    useEffect(() => {
        fetchComplaints();
    }, [fetchTrigger]); // The magic!

    // Function to update the status of a complaint
    const handleStatusChange = async (id, newStatus) => {
        try {
            await axios.put(`http://localhost:5001/api/complaints/${id}`, { status: newStatus });
            // Refresh the list after updating
            fetchComplaints(); 
        } catch (err) {
            console.error("Error updating status:", err);
        }
    };

    if (loading) {
        return <p>Loading complaints...</p>;
    }

    return (
        <div className="admin-dashboard">
            <h2>Admin Smart Dashboard</h2>
            <table>
                <thead>
                    <tr>
                        <th>Priority</th>
                        <th>Category</th>
                        <th>Complaint Details</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {complaints.map((complaint) => (
                        <tr key={complaint._id} className={`priority-${complaint.priority}`}>
                            <td>{complaint.priority}</td>
                            <td>{complaint.category}</td>
                            <td>{complaint.text}</td>
                            <td>{complaint.status}</td>
                            <td>
                                <select 
                                    value={complaint.status} 
                                    onChange={(e) => handleStatusChange(complaint._id, e.target.value)}
                                >
                                    <option value="New">New</option>
                                    <option value="In-Progress">In-Progress</option>
                                    <option value="Resolved">Resolved</option>
                                </select>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default AdminDashboard;
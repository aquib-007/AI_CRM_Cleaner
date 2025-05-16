import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [cleanedData, setCleanedData] = useState(null);
  const [error, setError] = useState(null);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/upload-csv/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail);
      }

      const data = await res.json();
      setCleanedData(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      setCleanedData(null);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>CRM Cleaner: Upload CSV</h1>
      <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} style={{ marginLeft: 10 }}>Upload & Clean</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {cleanedData && (
        <div style={{ marginTop: 20 }}>
          <h2>Cleaned Records</h2>
          <table border="1" cellPadding="8">
            <thead>
              <tr><th>Name</th><th>Email</th><th>Phone</th><th>Address</th></tr>
            </thead>
            <tbody>
              {cleanedData.map((rec, idx) => (
                <tr key={idx}>
                  <td>{rec.name}</td>
                  <td>{rec.email}</td>
                  <td>{rec.phone}</td>
                  <td>{rec.address}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;

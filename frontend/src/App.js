import React, { useState } from "react";
import OutputPage from "./components/OutputPage";
import axios from "axios";

function App() {
  const [cleanedData, setCleanedData] = useState(null);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post("http://localhost:8000/upload-csv/", formData);
    setCleanedData(response.data);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>CRM Cleaner</h1>
      <input type="file" accept=".csv" onChange={handleFileUpload} />
      {cleanedData && <OutputPage cleanedData={cleanedData} />}
    </div>
  );
}

export default App;

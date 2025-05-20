import React from "react";
import { exportToCSV } from "../utils/csvExport";

const OutputPage = ({ cleanedData }) => {
  if (!cleanedData || cleanedData.length === 0) {
    return <div>No cleaned data to display.</div>;
  }

  const headers = Object.keys(cleanedData[0]);

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Cleaned Data</h2>
      <button
        onClick={() => exportToCSV(cleanedData)}
        style={{
          marginBottom: "1rem",
          padding: "0.5rem 1rem",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Download CSV
      </button>

      <table
        style={{
          borderCollapse: "collapse",
          width: "100%",
          border: "1px solid #ddd",
        }}
      >
        <thead>
          <tr>
            {headers.map((header) => (
              <th
                key={header}
                style={{
                  border: "1px solid #ddd",
                  padding: "8px",
                  backgroundColor: "#f2f2f2",
                }}
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {cleanedData.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {headers.map((header) => (
                <td
                  key={header}
                  style={{ border: "1px solid #ddd", padding: "8px" }}
                >
                  {row[header]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default OutputPage;

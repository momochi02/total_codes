import React, { useState } from "react";

function Testrs({ result }) {
  const [copied, setCopied] = useState(null); // để theo dõi mục nào đã copy

  const handleCopy = async (title, data) => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(data, null, 2));
      setCopied(title);
      setTimeout(() => setCopied(null), 1500); // reset sau 1.5s
    } catch (err) {
      console.error("Lỗi khi copy:", err);
    }
  };

  const renderResultSection = (title, dataKey) => {
    const data = result?.[dataKey];
    return (
      <div
        style={{
          marginBottom: "20px",
          padding: "10px",
          border: "1px solid #ccc",
          borderRadius: "8px",
          backgroundColor: "#f9f9f9",
          position: "relative",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h4 style={{ color: "#2c3e50", margin: 0 }}>{title}</h4>
          <button
            onClick={() => handleCopy(title, data)}
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              fontSize: "16px",
              color: "#007bff",
            }}
            title="Copy JSON"
          >
            📋
          </button>
        </div>
        {copied === title && <div style={{ color: "green" }}>✅ Đã copy!</div>}
        <pre
          style={{
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
            backgroundColor: "#eef",
            padding: "10px",
            borderRadius: "5px",
            maxHeight: "300px",
            overflow: "auto",
            marginTop: "10px",
          }}
        >
          {data ? JSON.stringify(data, null, 2) : "⏳ ..."}
        </pre>
      </div>
    );
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>📄 Kết quả so sánh</h3>
      {renderResultSection("🧠 Gauss Result", "gauss")}
      {renderResultSection("📐 Logic Result", "logic")}
    </div>
  );
}

export default Testrs;

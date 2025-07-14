import React, { useState } from "react";
import "./ResultBox_css.css"; // Nhớ import file CSS

function ResultBox({ result }) {
  const [copied, setCopied] = useState(null);

  const handleCopy = async (title, data) => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(data, null, 2));
      setCopied(title);
      setTimeout(() => setCopied(null), 1500);
    } catch (err) {
      console.error("Lỗi khi copy:", err);
    }
  };

  const renderResultSection = (title, dataKey) => {
    const data = result?.[dataKey] || null;

    return (
      <div className="result-section">
        <div className="result-header">
          <h4>{title}</h4>
          {data && (
            <button
              className="copy-button"
              onClick={() => handleCopy(title, data)}
              title="Copy JSON"
            >
              📋
            </button>
          )}
        </div>
        {copied === title && <div className="copied-feedback">✅ Copied!</div>}
        <pre className="result-content">
          {data ? JSON.stringify(data, null, 2) : "⏳ Đang chờ kết quả..."}
        </pre>
      </div>
    );
  };

  return (
    <div className="result-container">
      <h3>📄 Kết quả so sánh</h3>
      {renderResultSection("🧠 Gauss Result", "gauss")}
      {renderResultSection("📐 Logic Result", "logic")}
    </div>
  );
}

export default ResultBox;

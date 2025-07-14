import React, { useState } from "react";
import "./FileUploadForm_css.css"; // ✅ Nhúng CSS riêng

function FileUploadForm({ onCompare }) {
  const [tabletFile, setTabletFile] = useState(null);
  const [phoneFile, setPhoneFile] = useState(null);
  const [promptFile, setPromptFile] = useState(null);

  const handleSubmit = (apiType) => {
    if (!tabletFile || !phoneFile) {
      alert("⚠️ Bạn cần chọn đủ Tablet XML và Phone XML!");
      return;
    }
    onCompare(tabletFile, phoneFile, promptFile, apiType);
  };

  return (
    <div className="file-upload-form">
      <div>
        <label>📱 File Tablet XML :*</label>
        <input
          type="file"
          accept=".xml"
          onChange={(e) => setTabletFile(e.target.files[0])}
        />
        {tabletFile && <div className="selected-file">📄 {tabletFile.name}</div>}
      </div>

      <div>
        <label>📞 File Phone XML :*</label>
        <input
          type="file"
          accept=".xml"
          onChange={(e) => setPhoneFile(e.target.files[0])}
        />
        {phoneFile && <div className="selected-file">📄 {phoneFile.name}</div>}
      </div>

      <div>
        <label>📝 File Prompt TXT:  </label>
        <input
          type="file"
          accept=".txt"
          onChange={(e) => setPromptFile(e.target.files[0])}
        />
        {promptFile && <div className="selected-file">📄 {promptFile.name}</div>}
      </div>

      <button class='compare-xml' onClick={() => handleSubmit("twoAPI_2")}>
        🚀 Ananazy
      </button>
    </div>
  );
}

export default FileUploadForm;

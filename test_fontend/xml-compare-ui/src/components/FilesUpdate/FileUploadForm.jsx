import React, { useState, useEffect } from "react";
import "./FileUploadForm_css.css"; // ✅ Nhúng CSS riêng

function FileUploadForm({ onCompare,loading }) {
  const [tabletFile, setTabletFile] = useState(null);
  const [phoneFile, setPhoneFile] = useState(null);
//      const [PromptFile, setPromptFile] = useState(null);

  const [promptContent, setPromptContent] = useState("");
  const [promptFileName, setPromptFileName] = useState("");

  // Load lại dữ liệu khi reload
  useEffect(() => {
    const pr = localStorage.getItem("promptContent");
    const prn = localStorage.getItem("promptFileName");

    if (pr) setPromptContent(pr);
    if (prn) setPromptFileName(prn);
  }, []);

  const handleFileChange = (e, setContent, setName, keyPrefix) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      setContent(reader.result);
      setName(file.name);
      localStorage.setItem(`${keyPrefix}Content`, reader.result);
      localStorage.setItem(`${keyPrefix}FileName`, file.name);
    };
    reader.readAsText(file);
  };

    const handleClearPrompt = () => {
      localStorage.removeItem("promptContent");
      localStorage.removeItem("promptFileName");
      setPromptContent("");
      setPromptFileName("");
    };

  const handleSubmit = (apiType) => {
    if (!tabletFile || !phoneFile) {
      alert("⚠️ Bạn cần chọn đủ Tablet XML và Phone XML!");
      return;
    }

    onCompare(tabletFile, phoneFile, promptContent, apiType); // Gửi prompt dưới dạng string
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
        {tabletFile && <label className="selected-file">📄 {tabletFile.name}</label>}
      </div>

      <div>
        <label>📞 File Phone XML :*</label>
        <input
          type="file"
          accept=".xml"
          onChange={(e) => setPhoneFile(e.target.files[0])}
        />
        {phoneFile && <label className="selected-file">📄 {phoneFile.name}</label>}
      </div>


       <div>

          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <label>📝 File Prompt TXT:</label>
            <input
              type="file"
              accept=".txt"
              onChange={(e) =>
                handleFileChange(e, setPromptContent, setPromptFileName, "prompt")
              }
            />
            {promptFileName && (
              <>

<a
  href={`data:text/plain;charset=utf-8,${encodeURIComponent(promptContent)}`}
  download={promptFileName || "prompt.txt"}
>
  ⬇️ Tải lại prompt
</a>
                <button className="clear-button" onClick={handleClearPrompt}>
                  🗑
                </button>
              </>
            )}
          </div>
        </div>

     <button
          className="compare-xml"
          onClick={() => handleSubmit("twoAPI_2")}
          disabled={loading}
        >
          {loading ? "⏳ Đang xử lý..." : "🚀 Ananazy"}
        </button>
    </div>
  );
}

export default FileUploadForm;

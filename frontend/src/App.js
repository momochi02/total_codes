import React, { useState } from "react";
import axios from "axios";

function App() {
  const [tabletFile, setTabletFile] = useState(null);
  const [phoneFile, setPhoneFile] = useState(null);
  const [result, setResult] = useState(null);
  const makeFormData = () => {
      const fd = new FormData();
      fd.append("tablet_xml", tabletFile);
      fd.append("phone_xml", phoneFile);
      return fd;
    };

  const handleSubmit = async (apiType) => {
    if (!tabletFile || !phoneFile) {
      alert("Vui lòng chọn cả hai file XML.");
      return;
    }

    const url_gauss = "http://127.0.0.1:8000/compare_xml_by_gauss";
    const url_logic_code = "http://127.0.0.1:8000/compare_xml_by_logic_code";

   formData1  = makeFormData()
   formData2  = makeFormData()
//    const formData = new FormData();
//    formData.append("tablet_xml", tabletFile);
//    formData.append("phone_xml", phoneFile);

    try {
      if (apiType === "twoAPI_1") {
        // Gọi tuần tự
        const response_gauss = await axios.post(url_gauss, formData1, {
          headers: {
            "x-api-key": "key_pc1",
            "Content-Type": "multipart/form-data",
          },
        });

        const response_logic = await axios.post(url_logic_code, formData2, {
          headers: {
            "x-api-key": "key_pc1",
            "Content-Type": "multipart/form-data",
          },
        });

        setResult({
          gauss: response_gauss.data,
          logic: response_logic.data,
        });
      } else if (apiType === "twoAPI_2") {
        // Gọi song song
        const [response_gauss, response_logic] = await Promise.all([
          axios.post(url_gauss, formData1, {
            headers: {
              "x-api-key": "key_pc1",
              "Content-Type": "multipart/form-data",
            },
          }),
          axios.post(url_logic_code, formData2, {
            headers: {
              "x-api-key": "key_pc1",
              "Content-Type": "multipart/form-data",
            },
          }),
        ]);

        setResult({
          gauss: response_gauss.data,
          logic: response_logic.data,
        });
      } else {
        // Gọi 1 trong 2 API
        const endpoint = apiType === "gauss" ? url_gauss : url_logic_code;

        const response = await axios.post(endpoint, formData1, {
          headers: {
            "x-api-key": "key_pc1",
            "Content-Type": "multipart/form-data",
          },
        });

        setResult(response.data);
      }
    } catch (err) {
      console.error(err);
      setResult({ error: "Lỗi khi gửi file hoặc từ server." });
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>So sánh XML</h2>

      <div>
        <label>File Tablet XML: </label>
        <input type="file" accept=".xml" onChange={(e) => setTabletFile(e.target.files[0])} />
      </div>

      <div>
        <label>File Phone XML: </label>
        <input type="file" accept=".xml" onChange={(e) => setPhoneFile(e.target.files[0])} />
      </div>

      <br />

      <button onClick={() => handleSubmit("logic")} style={{ marginRight: "10px" }}>
        So sánh bằng Logic Code
      </button>
      <button onClick={() => handleSubmit("gauss")} style={{ marginRight: "10px" }}>
        So sánh bằng Gauss
      </button>

      <br /><br />

      <button onClick={() => handleSubmit("twoAPI_1")} style={{ marginRight: "10px" }}>
        Gọi 2 API (tuần tự)
      </button>
      <button onClick={() => handleSubmit("twoAPI_2")}>
        Gọi 2 API (song song)
      </button>

      {result && (
        <div>
          <h3>Kết quả:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;

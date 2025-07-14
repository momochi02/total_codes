import React, { useState } from "react";
import axios from "axios";
import FileUpload from "../components/FilesUpdate/FileUploadForm";
import ResultBox from "../components/ResultBoxs/ResultBox";
import Testrs from "../components/ResultBoxs/Testrs";
function Compare() {
  const [result, setResult] = useState(null);

  const handleCompare = async (tabletXml, phoneXml, prompt_txt = null, apiType = "gauss") => {
    const makeFormData = () => {
      const fd = new FormData();
      fd.append("tablet_xml", tabletXml);
      fd.append("phone_xml", phoneXml);
      if (prompt_txt instanceof File) {
        fd.append("prompt_txt", prompt_txt);
      }
      return fd;
    };
    console.log("📤 tabletXml:", tabletXml?.name);
    console.log("📤 phoneXml:", phoneXml?.name);
    console.log("📤 prompt_txt:", prompt_txt?.name);

    const headers = {
      "x-api-key": "key_pc1",
//       "Content-Type": "multipart/form-data",
    };

    const formDataGauss = makeFormData();
    const formDataLogic = makeFormData();

    const url_gauss = "http://127.0.0.1:8000/compare_xml_by_gauss";
    const url_logic_code = "http://127.0.0.1:8000/compare_xml_by_logic_code";

    try {
      if (apiType === "twoAPI_1") {
        // Gọi lần lượt
        const response_gauss = await axios.post(url_gauss, formDataGauss, { headers });
        const response_logic = await axios.post(url_logic_code, formDataLogic, { headers });

        setResult({
          gauss: response_gauss.data,
          logic: response_logic.data,
        });

      } else if (apiType === "twoAPI_2") {
        // Gọi song song
        const [response_gauss, response_logic] = await Promise.all([
          axios.post(url_gauss, formDataGauss, { headers }),
          axios.post(url_logic_code, formDataLogic, { headers }),
        ]);

        setResult({
          gauss: response_gauss.data,
          logic: response_logic.data,
        });

      } else {
        // Gọi một API
        const endpoints = {
          gauss: url_gauss,
          logic: url_logic_code,
        };

        const response = await axios.post(endpoints[apiType], formDataGauss, { headers });
        setResult(response.data);
      }
    } catch (err) {
      console.error("❌ Lỗi chi tiết:", err);
        if (err.response) {
          console.error("📡 Response data:", err.response.data);
          console.error("📡 Status:", err.response.status);
          console.error("📡 Headers:", err.response.headers);
        }

      setResult({ error: "Lỗi khi gửi file hoặc từ server." });
    }
  };

  return (
    <div>
      <h2>📄 So sánh XML</h2>
      <FileUpload onCompare={handleCompare} />
{/*      <ResultBox result={result} /> */}
      <Testrs result={result} />
    </div>
  );
}

export default Compare;

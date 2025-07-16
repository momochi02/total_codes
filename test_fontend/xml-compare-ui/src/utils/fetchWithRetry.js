// utils/fetchWithRetry.js
import axios from "axios";
export async function fetchWithRetry(url, options = {}, maxRetries = 3, delay = 1000) {
  let attempt = 0;
  while (attempt < maxRetries) {
    try {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`Server trả về lỗi ${response.status}`);
      }
      return response;
    } catch (error) {
      attempt++;
      console.warn(`⏳ Thử lần ${attempt}/${maxRetries}: ${error.message}`);
      if (attempt >= maxRetries) {
        throw new Error("❌ Gửi request thất bại sau nhiều lần thử.");
      }
      await new Promise((res) => setTimeout(res, delay)); // đợi delay ms
    }
  }
}

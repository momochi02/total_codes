export async function fetchWithRetry(url, data = {}, config = {}, maxRetries = 3, delay = 1000) {
  let attempt = 0;
  while (attempt < maxRetries) {
    try {
      const response = await axios.post(url, data, config);
      return response;
    } catch (error) {
      attempt++;
      console.warn(`⏳ Thử lần ${attempt}/${maxRetries}: ${error.message}`);
      if (attempt >= maxRetries) {
        throw new Error("❌ Gửi request thất bại sau nhiều lần thử.");
      }
      await new Promise((res) => setTimeout(res, delay));
    }
  }
}

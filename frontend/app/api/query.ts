// app/api/query.ts
import axios from "axios";

const API_URL = "http://localhost:8000";

export const askQuery = async (query: string) => {
  try {
    const response = await axios.post(`${API_URL}/ask`, { query });
    return response.data.response;
  } catch (error) {
    console.error("Error:", error);
    return "Sorry, I couldn't process your request.";
  }
};
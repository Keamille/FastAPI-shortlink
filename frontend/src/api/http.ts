import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL ?? "";

export const http = axios.create({
  baseURL,
  timeout: 10_000,
  headers: { "Content-Type": "application/json" },
});

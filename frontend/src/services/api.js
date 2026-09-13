import axios from "axios";

const API = "https://ai-finance-assistant-btxp.onrender.com";

export const registerUser = async (userData) => {
  const response = await API.post("/register", userData);
  return response.data;
};

export const loginUser = async (userData) => {
  const response = await API.post("/login", userData);
  return response.data;
};

export const getTransactions = async (userId) => {
  const response = await API.get(`/transactions/${userId}`);
  return response.data;
};

export const getDashboard = async (userId) => {
  const response = await API.get(`/dashboard/${userId}`);
  return response.data;
};

export const getBudgets = async (userId) => {
  const response = await API.get(`/budgets/${userId}`);
  return response.data;
};

export default API;
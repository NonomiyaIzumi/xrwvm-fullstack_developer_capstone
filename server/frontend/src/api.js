const API_BASE = "/djangoapp";

async function apiGet(path) {
  const response = await fetch(`${API_BASE}${path}`, { credentials: "same-origin" });
  return response.json();
}

async function apiPost(path, body) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify(body),
  });
  return response.json();
}

export const getCurrentUser = () => window.__DEALERSHIP_USER__ || { isAuthenticated: false, username: "" };

export const fetchDealers = (state) => apiGet(state && state !== "All" ? `/get_dealers/${state}` : "/get_dealers");
export const fetchDealer = (id) => apiGet(`/dealer/${id}`);
export const fetchDealerReviews = (id) => apiGet(`/reviews/dealer/${id}`);
export const fetchCarModels = () => apiGet("/get_cars");

export const login = (userName, password) => apiPost("/login", { userName, password });
export const logout = () => apiGet("/logout");
export const register = (payload) => apiPost("/register", payload);
export const addReview = (payload) => apiPost("/add_review", payload);

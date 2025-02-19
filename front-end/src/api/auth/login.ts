import { apiEndpoints } from "@/api/apiEndpoints";
import { errorStatus } from "@/api/standardError";
export const loginFetch = async (credentials: Record<string, string>) => {
  const response = await fetch(apiEndpoints.auth.login, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });
  errorStatus(401);
  if (!response.ok) {
    const errorData = await response.json();
    console.log(errorData);
    throw new Error(errorData.message || "An error occurred");
  }
  return response.json();
};
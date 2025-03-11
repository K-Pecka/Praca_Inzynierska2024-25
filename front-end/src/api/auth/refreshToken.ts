import { TOKEN } from "@/type/interface";
import { apiEndpoints } from "@/api/apiEndpoints";
export const fetchRefreshToken = async (token: TOKEN) => {
  // try {
    const response = await fetch(apiEndpoints.auth.refreshToken, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: token.refresh }),
    });
    console.log("weryfikacja");
    console.count("weryfikacja");
    if (!response.ok) {
      throw new Error("An error occurred");
    }

    return response.json();
  // } catch (error: unknown) {
  //   if (error instanceof Error) {
  //     console.error("Error refreshing token:", error.message);
  //     throw error;
  //   }
  // }
};

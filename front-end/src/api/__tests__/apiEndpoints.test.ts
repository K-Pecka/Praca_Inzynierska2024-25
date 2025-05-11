// import { describe, it, expect, vi } from "vitest";
// import {
//   fetchData,
//   setParam,
//   apiEndpoints,
// } from "@/api/apiEndpoints";
// const token = "testToken";
// vi.mock("@/stores", () => ({
//   useAuthStore: vi.fn().mockReturnValue({
//     getToken: vi.fn().mockReturnValue({
//       access: "testToken",
//     }),
//   }),
// }));

// const getRandomError = () => {
//   const errors = ["Network Error", "Timeout Error", "Forbidden"];
//   return errors[Math.floor(Math.random() * errors.length)];
// };

// const getRandomJsonResponse = () => {
//   const responses = [
//     { message: "Success" },
//     { message: "Server Error" },
//     { message: "Unauthorized" },
//   ];
//   return responses[Math.floor(Math.random() * responses.length)];
// };

// describe("fetchData function", () => {
//   it("should call fetch with correct parameters and return data", async () => {
//     const mockJsonResponse = getRandomJsonResponse();

//     globalThis.fetch = vi.fn().mockResolvedValue({
//       ok: true,
//       json: vi.fn().mockResolvedValue(mockJsonResponse),
//     });

//     const url = `${hostName}/trip/all/`;
//     const options = { body: undefined };
//     const method = "GET";

//     const result = await fetchData(url, options, method);

//     expect(globalThis.fetch).toHaveBeenCalledWith(
//       url,
//       expect.objectContaining({
//         method: method,
//         headers: expect.objectContaining({
//           Authorization: "Bearer testToken",
//         }),
//         body: undefined,
//       })
//     );

//     expect(result.data).toEqual(mockJsonResponse);
//   });

//   it("should return error message if fetch fails", async () => {
//     const randomError = getRandomError();

//     globalThis.fetch = vi.fn().mockRejectedValue(new Error(randomError));

//     const result = await fetchData(`${hostName}/trip/all/`);

//     expect(result.error).toBe(randomError);
//   });

//   it("should handle non-200 response correctly", async () => {
//     const mockJsonResponse = getRandomJsonResponse();

//     globalThis.fetch = vi.fn().mockResolvedValue({
//       ok: false,
//       json: vi.fn().mockResolvedValue(mockJsonResponse),
//     });

//     const result = await fetchData(`${hostName}/trip/all/`);

//     expect(result.error).toBe(mockJsonResponse.message);
//   });
// });

// describe("setParam function", () => {
//   it("should replace placeholders with actual params", () => {
//     const url = `${hostName}/trip/:tripId/detail/`;
//     const params = { tripId: "123" };
//     const result = setParam(url, params);

//     expect(result).toBe(`${hostName}/trip/123/detail/`);
//   });
//   it("should replace placeholders with random params", () => {
//     const url = `${hostName}/trip/:tripId/detail/`;
//     const randomTripId = Math.floor(Math.random() * 1000).toString();
//     const params = { tripId: randomTripId };
//     const result = setParam(url, params);

//     expect(result).toBe(`${hostName}/trip/${randomTripId}/detail/`);
//   });
//   it("should replace placeholders with existing params and warn for missing params", () => {
//     const url = `${hostName}/trip/:tripId/detail/`;
//     const randomTripId = Math.floor(Math.random() * 1000).toString();
//     const params = { dontExist: randomTripId };
//     const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});
  
//     const result = setParam(url, params);
  
//     expect(spy).toHaveBeenCalledWith('Missing parameter: dontExist');
    
//     expect(result).toBe(`${hostName}/trip/:tripId/detail/`);
  
//     spy.mockRestore();
//   });;
// });

// describe("API Endpoints", () => {
//   it("should define correct API endpoint for login", () => {
//     expect(apiEndpoints.auth.login).toBe(`${hostName}/user_auth/login/`);
//   });

//   it("should define correct API endpoint for trip detail", () => {
//     expect(apiEndpoints.trip.detail).toBe(`${hostName}/trip/:tripId/`);
//   });
// });

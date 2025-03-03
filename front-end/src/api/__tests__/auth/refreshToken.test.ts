import { describe, it, expect, vi } from 'vitest';
import { fetchRefreshToken } from '@/api';
import { apiEndpoints} from "@/api/apiEndpoints";
import { TOKEN } from "@/type/interface";

vi.mock("@/stores", () => ({
  useAuthStore: vi.fn().mockReturnValue({
    getToken: vi.fn().mockReturnValue({
      refresh: 'valid-refresh-token',
      access: "testToken",
    }),
  }),
}));

describe('fetchRefreshToken function', () => {
  it('should send POST request to refresh token and return response JSON', async () => {
    const mockToken: TOKEN = { refresh: 'valid-refresh-token'};
    const mockResponse: TOKEN = { refresh: 'new-access-token', access: "" };
    
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: vi.fn().mockResolvedValueOnce(mockResponse),
    });

    const result = await fetchRefreshToken(mockToken);

    expect(globalThis.fetch).toHaveBeenCalledWith(apiEndpoints.auth.refreshToken, expect.objectContaining({
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(mockToken),
    }));

    expect(result).toEqual(mockResponse);
  });

  it('should throw an error if the response is not ok', async () => {
    const mockToken: TOKEN = { refresh: 'valid-refresh-token' };

  globalThis.fetch = vi.fn().mockResolvedValueOnce({
    ok: false,
    json: vi.fn().mockResolvedValueOnce({ message: 'Error' }),
  });

  await expect(fetchRefreshToken(mockToken)).rejects.toThrow('An error occurred');
  });
});

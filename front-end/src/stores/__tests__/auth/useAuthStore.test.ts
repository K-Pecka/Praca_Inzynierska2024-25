import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '@/stores';
import { useNotificationStore } from '@/stores/ui/useNotificationStore';
import router from '@/router';
import { fetchVerify, fetchRefreshToken, loginFetch, registerFetch } from '@/api/endpoints/auth';

vi.mock('@/api/auth', async () => {
  return {
    fetchVerify: vi.fn().mockResolvedValue(true),
    fetchRefreshToken: vi.fn().mockResolvedValue({ access: 'new_access', refresh: 'new_refresh' }),
    loginFetch: vi.fn().mockResolvedValue({ access: 'access_token', refresh: 'refresh_token' }),
    registerFetch: vi.fn().mockResolvedValue({ message: 'Success' }),
  };
});

vi.mock('@/router', () => ({
    default: {
      push: vi.fn(),
    },
  }));

vi.mock('@/stores/ui/useNotificationStore', () => ({
  useNotificationStore: () => ({
    loginSuccess: vi.fn(),
    setErrorCurrentMessage: vi.fn(),
    setSuccessCurrentMessage: vi.fn(),
    logOutSuccess: vi.fn(),
  }),
}));
vi.mock('@tanstack/vue-query', () => ({
    useMutation: vi.fn(() => ({
      mutate: vi.fn(),
    })),
    useQueryClient: vi.fn(() => ({
      invalidateQueries: vi.fn(),
    })),
  }));
describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('should initialize with no token', () => {
    const store = useAuthStore();
    expect(store.token).toBe(null);
  });

  it('should save and retrieve token', () => {
    const store = useAuthStore();
    const mockToken = { access: 'access_token', refresh: 'refresh_token' };
    store.saveToken(mockToken);
    expect(store.getToken()).toEqual(mockToken);
  });

  it('should logout and clear token', () => {
    const store = useAuthStore();
    store.token = { access: 'access_token', refresh: 'refresh_token' };
    store.logout();
    expect(store.token).toBe(null);
    expect(router.push).toHaveBeenCalledWith({ name: 'landing' });
  });

  it('should verify token correctly', async () => {
    const store = useAuthStore();
    globalThis.fetch = vi.fn().mockResolvedValueOnce(true);
    store.token = { access: 'valid_token', refresh: 'refresh_token' };
    const result = await store.validToken();
    expect(result).toBe(true);
    expect(fetchVerify).toHaveBeenCalledWith({ access: 'valid_token', refresh: 'refresh_token' });
  });

//   it('should handle token refresh', async () => {
//     const store = useAuthStore();
//     const newToken = { access: 'new_access', refresh: 'new_refresh' };
//     globalThis.fetch = vi.fn().mockResolvedValueOnce(newToken);
//     store.token = { access: 'old_access', refresh: 'old_refresh' };
//     const result = await store.refreshToken();
//     expect(result).toBe(true);
//     expect(store.getToken()).toEqual(newToken);
// });

});

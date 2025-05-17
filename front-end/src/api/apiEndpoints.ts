export const backendNotification = false;
import apiClient from './apiClient';

export const fetchData = async <T = unknown>(
    url: string,
    method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' = 'GET',
    data?: any
): Promise<{ data?: T; error?: string }> => {
  try {
    const response = await apiClient.request<T>({
      url,
      method,
      data,
    });
    return { data: response.data };
  } catch (error: any) {
    return {
      error: error.response?.data?.message || error.message || 'Wystąpił błąd',
    };
  }
};
export const setParam = (
  url: string,
  params: Record<string, string>
): string => {
  return Object.keys(params).reduce((acc, key) => {
    if (acc.includes(`:${key}`)) {
      return acc.replace(`:${key}`, encodeURIComponent(params[key]));
    } else {
      return acc;
    }
  }, url);
};

export const apiEndpoints = {
  user: {
    update:`/user/update/`,
    getUserById: `/user/user/by-profile/:userId/`,
  },
  auth: {
    login: `/user_auth/login/`,
    register: `/user/create/`,
    refreshToken: `/user_auth/token/refresh/`,
    verify: `/user_auth/token/verify/`,
    profile: `/user/profile/`,
    logout: `/user_auth/logout/`,
  },
  expense: {
    all: `/trip/:tripId/expense/all/`,
    detail: `/trip/:tripId/expense/:expenseId/`,
    delete: `/trip/:tripId/expense/:expenseId/delete/`,
    create: `/trip/:tripId/expense/create/`,
  },
  trip: {
    all: `/trip/all/`,
    detail: `/trip/:tripId/`,
    delete: `/trip/:tripId/delete/`,
    create: `/trip/create/`,
    update: `/trip/:tripId/update/`,
    inviteUser: `/trip/:tripId/participants/manage/`,
  },
  plan: {
    all: `/trip/:tripId/itinerary/all/`,
    detail: `/trip/:tripId/itinerary/:planId/`,
    delete: `/trip/:tripId/itinerary/:planId/delete/`,
    create: `/trip/:tripId/itinerary/create/`,
  },
  activity: {
    all: `/trip/:tripId/itinerary/:planId/activities/all/`,
    detail: `/trip/:tripId/activity/:activityId/`,
    delete: `/trip/:tripId/itinerary/:planId/activities/:activityId/delete/`,
    create: `/trip/:tripId/itinerary/:planId/activities/create/`,
  },
  activityType: {
    all: `/trip/:tripId/itinerary/activity-types/all/`,
  },
  ticket: {
    create: `/trip/:tripId/ticket/create/`,
    all: `/trip/:tripId/ticket/all/`,
    delete: `/trip/:tripId/ticket/:ticketId/delete/`,
  },
  budget: {
    update: `/trip/:tripId/budget/update/`,
  },
};

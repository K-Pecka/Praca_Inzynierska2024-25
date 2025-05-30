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
      error: error.response.data || 'Wystąpił błąd',
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
    role: `/user/profile/:role/change-default/`,
  },
  pay: `/payment/create-checkout-session/`,
  auth: {
    login: `/user_auth/login/`,
    register: `/user/create/`,
    refreshToken: `/user_auth/token/refresh/`,
    verify: `/user_auth/token/verify/`,
    profile: `/user/profile/`,
    logout: `/user_auth/logout/`,
  },
  expense: {
    all: `/trip/:tripId/expenses/`,
    detail: `/trip/:tripId/expenses/:expenseId/`,
    delete: `/trip/:tripId/expenses/:expenseId/`,
    create: `/trip/:tripId/expenses/`,
  },
  debt:{
    all: `/trip/:tripId/debt/`,
    create: `/trip/:tripId/debt/`,
    delete: `/trip/:tripId/debt/:debtId/`,
    removeMember: `/trip/:tripId/debt/:debtId/remove-member/`
  },
  trip: {
    all: `/trip/`,
    detail: `/trip/:tripId/`,
    delete: `/trip/:tripId/`,
    create: `/trip/`,
    update: `/trip/:tripId/`,
    inviteUser: `/trip/:tripId/participants/manage/`,
  },
  plan: {
    all: `/trip/:tripId/itinerary/`,
    detail: `/trip/:tripId/itinerary/:itineraryId/`,
    delete: `/trip/:tripId/itinerary/:itineraryId/`,
    create: `/trip/:tripId/itinerary/`,
  },
  activity: {
    all: `/trip/:tripId/itinerary/:itineraryId/activities/`,
    detail: `/trip/:tripId/itinerary/:itineraryId/activities/:activityId/`,
    delete: `/trip/:tripId/itinerary/:itineraryId/activities/:activityId/`,
    create: `/trip/:tripId/itinerary/:itineraryId/activities/`,
  },
  activityType: {
    all: `/trip/:tripId/itinerary/activity-types/`,
  },
  ticket: {
    all: `/trip/:tripId/ticket/`,
    create: `/trip/:tripId/ticket/`,
    delete: `/trip/:tripId/ticket/:ticketId/`,
    updateMembers: '/trip/:tripId/ticket/:ticketId/'
  },
  budget: {
    update: `/trip/:tripId/budget/update/`,
  },
};

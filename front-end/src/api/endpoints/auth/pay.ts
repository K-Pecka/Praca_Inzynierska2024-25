import { apiEndpoints, fetchData } from "@/api/apiEndpoints";

export const fetchPaymentUrl = async (priceId: string) => {
  const { data, error } = await fetchData(
    apiEndpoints.pay.payment,
    "POST",
    { price_id: priceId }
  );

  if (error) {
    throw error;
  }

  return data as { checkout_url: string};
};

export const fetchSubscriptionCancel = async () => {
  const { data, error } = await fetchData(
    apiEndpoints.pay.cancel,
    "GET",
  );

  if (error) {
    throw error;
  }

  return data as { checkout_url: string};
};

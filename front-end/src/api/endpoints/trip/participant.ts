import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
export const fetchAddParticipant = async (
  idTrip: number,
  participant: { name: string; email: string }
) => {
  const { data, error } = await fetchData(
    setParam(`${apiEndpoints.trip.invateUser}?action=invite`, { tripId: String(idTrip) }),
    {body: JSON.stringify(participant)},
    "PUT"
  );
  if (error) {
    throw new Error(error);
  }

  return idTrip;
};
export const fetchRemoveParticipant = async (
  idTrip: number,
  idParticipant: number
) => {
  const { data, error } = await fetchData(
    setParam(`${apiEndpoints.trip.invateUser}?action=remove`, { tripId: String(idTrip) }),
    {body: JSON.stringify({ 'profile_id': idParticipant })},
    "PUT"
  );
  if (error) {
    throw new Error(error);
  }

  return idTrip;
};

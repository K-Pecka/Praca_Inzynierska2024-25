import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";

export const fetchAddParticipant = async (
    idTrip: number,
    participant: { email: string }
) => {
  const url = setParam(`${apiEndpoints.trip.inviteUser}?action=invite`, {
    tripId: String(idTrip),
  });

  const { data, error } = await fetchData(url, "PUT", participant);

  if (error) {
    throw error;
  }

  return idTrip;
};

export const fetchRemoveParticipant = async (
    idTrip: number,
    idParticipant: number
) => {
  const url = setParam(`${apiEndpoints.trip.inviteUser}?action=remove`, {
    tripId: String(idTrip),
  });

  const { data, error } = await fetchData(url, "PUT", {
    profile_id: idParticipant,
  });

  if (error) {
    throw error;
  }

  return idTrip;
};

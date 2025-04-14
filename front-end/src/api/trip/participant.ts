import { apiEndpoints, fetchData, setParam } from "../apiEndpoints";
import { useMockupStore } from "@/mockup/useMockupStore";
import { APP_MODE_DEV } from "@/config/envParams";
export const fetchAddParticipant = async (
  idTrip: number,
  participant: { name: string; email: string }
) => {
  if (APP_MODE_DEV) {
    const { addParticipant } = useMockupStore();
    const participantAdd = addParticipant(idTrip, participant);
    if (participantAdd?.error) {
      throw new Error(participantAdd.message);
    }
    return participantAdd;
  }
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
  if (APP_MODE_DEV) {
    const { removeParticipant } = useMockupStore();
    const participant = removeParticipant(idTrip, idParticipant);
    if (participant?.error) {
      throw new Error(participant.message);
    }
    return participant;
  }
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

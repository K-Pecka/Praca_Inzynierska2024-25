import {useMutation, useQueryClient} from "@tanstack/vue-query";
import {fetchAddParticipant, fetchRemoveParticipant} from "@/api";
import {useNotificationStore} from "@/stores";

export const useParticipants = () => {
    const queryClient = useQueryClient();
    const notifications = useNotificationStore();

    const addParticipantMutation = useMutation({
        mutationFn: ({idTrip, participant}: {
            idTrip: number, participant: { email: string }
        }) => fetchAddParticipant(idTrip, participant),
        onSuccess: (idTrip) => {
            notifications.setSuccessCurrentMessage("Dodano uczestnika");
            queryClient.refetchQueries({ queryKey: ["trip", idTrip] });
        },
        onError: (err: any) =>
            notifications.setErrorCurrentMessage(err.message || "Błąd"),
    });

    const removeParticipantMutation = useMutation({
        mutationFn: ({idTrip, idParticipant}: {
            idTrip: number; idParticipant: number;
        }) => fetchRemoveParticipant(idTrip, idParticipant),
        onSuccess: (idTrip) => {
            notifications.setSuccessCurrentMessage("Usunięto uczestnika");
            queryClient.refetchQueries({ queryKey: ["trip", idTrip] });
        },
        onError: (err: any) =>
            notifications.setErrorCurrentMessage(err.message || "Błąd"),
    });

    const addParticipant = (
        idTrip: number,
        participant: { email: string }
    ) => addParticipantMutation.mutateAsync({idTrip, participant});

    const removeParticipant = (idTrip: number, idParticipant: number) =>
        removeParticipantMutation.mutateAsync({idTrip, idParticipant});

    return {addParticipant, removeParticipant};
};

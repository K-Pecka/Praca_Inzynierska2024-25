import {useMutation, useQueryClient} from "@tanstack/vue-query";
import {fetchAddParticipant, fetchRemoveParticipant} from "@/api";
import {useAuthStore, useNotificationStore, useUserStore, useUtilsStore} from "@/stores";
import router from "@/router";

export const useParticipants = () => {
    const queryClient = useQueryClient();
    const notifications = useNotificationStore();
    const {userData} = useAuthStore()
    const {getActiveProfile} = userData;
    const {getRole} = useUtilsStore()
    const addParticipantMutation = useMutation({
        mutationFn: ({idTrip, participant}: {
            idTrip: number, participant: { email: string }
        }) => fetchAddParticipant(idTrip, participant),
        onSuccess: (idTrip) => {
            notifications.setSuccessCurrentMessage("Dodano uczestnika");
            queryClient.refetchQueries({ queryKey: ["trip", idTrip] });
        },
        onError: (err: any) =>
            notifications.setErrorCurrentMessage(JSON.parse(err.error.replace(/'/g, '"'))[0] || err?.error || "Błąd"),
    });

    const removeParticipantMutation = useMutation({
        mutationFn: ({idTrip, idParticipant}: {
            idTrip: number; idParticipant: number;
        }) => fetchRemoveParticipant(idTrip, idParticipant),
        onSuccess: ({idTrip,idParticipant}) => {
            queryClient.refetchQueries({ queryKey: ["trip", idTrip] });
            if(idParticipant == getActiveProfile()?.id)
            {
                notifications.setSuccessCurrentMessage("Pomyślnie opuściłeś wycieczkę!");
                queryClient.refetchQueries({ queryKey: ["trips", getRole()] });
                router.push({name:"ChooseTrip",params:{role:getRole()}})
                return
            }
            notifications.setSuccessCurrentMessage("Usunięto uczestnika");
        },
        onError: (err: any) =>
            notifications.setErrorCurrentMessage(err?.message || err?.error || err?.detail || "Błąd"),
    });

    const addParticipant = (
        idTrip: number,
        participant: { email: string }
    ) => addParticipantMutation.mutateAsync({idTrip, participant});

    const removeParticipant = (idTrip: number, idParticipant: number) =>
        removeParticipantMutation.mutateAsync({idTrip, idParticipant});

    return {addParticipant, removeParticipant};
};

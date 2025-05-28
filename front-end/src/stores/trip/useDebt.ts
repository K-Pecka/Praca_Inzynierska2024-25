import { useQueryClient } from "@tanstack/vue-query";
import { useNotificationStore } from "@/stores";
import {
  getMutationDebtCreate,
  getDebtQuery,
  getMutationRemoveMemberQuery,
  getMutationDeleteDebt
} from "@/api/services/debtQuery";

export const useDebt = (tripId: Function) => {
  
  const notification = useNotificationStore();
  const queryClient = useQueryClient();
  const getDebt = (id?:number) => {
    const {
      data: debt,
      isLoading: isLoading_debt,
      error: error_debt,
      refetch: refetch_debt
    } = getDebtQuery(id || tripId());
    return {
      debt,
      isLoading_debt,
      error_debt,
      refetch_debt
    };
  }
  const createDebt = getMutationDebtCreate({
    notification,
    queryClient,
    successMessage: "Pomyślnie dodano wydatek",
    errorMessage: "Nie udało się dodać wydatku",
  });
  const removeMember = getMutationRemoveMemberQuery({
    notification,
    queryClient,
    successMessage: "Pomyślnie usunięto dłużnika",
    errorMessage: "Nie udało się usunąć dłużnika",
  })
  const deleteDebt = getMutationDeleteDebt({
    notification,
    queryClient,
    successMessage: "Pomyślnie usunięto dług",
    errorMessage: "Nie udało się usunąć długu",
  })
  return {
    removeMember,
    createDebt,
    getDebt,
    deleteDebt
  };
};

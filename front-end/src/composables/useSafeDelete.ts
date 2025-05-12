import { ref } from "vue";
import type SafeConfirmDialog from "@/components/SafeConfirmDialog.vue";

type ConfirmOptions = {
  title?: string;
  message?: string;
  wordToConfirm?: string;
};

const dialogRef = ref<InstanceType<typeof SafeConfirmDialog> | null>(null);

export function useSafeDelete() {
  const confirmAndRun = async (
    callback: () => void,
    options?: ConfirmOptions
  ) => {
    const confirmed = await dialogRef.value?.open(options);
    if (confirmed) callback();
  };

  return {
    dialogRef,
    confirmAndRun,
  };
}

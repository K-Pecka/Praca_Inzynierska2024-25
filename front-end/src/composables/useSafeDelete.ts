import { ref } from "vue";
import type SafeConfirmDialog from "@/components/shared/SafeConfirmDialog.vue";

type ConfirmOptions = {
  title?: string;
  message?: string;
  wordToConfirm?: string;
};

const dialogRef = ref<InstanceType<typeof SafeConfirmDialog> | null>(null);

export function useSafeDelete() {
  const confirmAndRun: (callback: () => void, options?: ConfirmOptions) => Promise<void> = async (
    callback,
    options
  ) => {
    const confirmed = await dialogRef.value?.open(options);
    if (confirmed) callback();
  };

  return {
    dialogRef,
    confirmAndRun,
  };
}

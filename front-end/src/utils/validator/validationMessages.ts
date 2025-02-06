import { useMessageStore } from "@/stores/messageStore";

export const getDefaultMessages = () => {
    const { getValidationRules } = useMessageStore();
    return getValidationRules();
  };
import {PricingPlanType} from "./types"
export interface PricingCard {
  type: PricingPlanType | null;
  name: string;
  price: string;
  features: string[];
  buttonVariant?: "primary" | "secondary";
  contentVariant?: "primary" | "secondary";
}
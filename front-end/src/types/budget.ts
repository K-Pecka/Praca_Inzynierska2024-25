export interface Expense {
  id?: number;
  trip?: number;
  title: string;
  amount: number;
  currency: string;
  date: string;
  user: number;
  category: number;
  note?: string;
  username?: string;
  converted_amount?: string;
}

export interface ExpenseResponse {
  results: Expense[];
}

export interface Budget {
  budget_amount: number;
}

export interface BudgetData {
  amount: number;
  currency: string;
  expenses: number;
}

<script setup lang="ts">
import { computed, ref } from "vue";
import AppButton from "@/components/AppButton.vue";
import { VDateInput } from "vuetify/labs/components";
import { budget } from "@/data/category/budget";
const categoryBudget = budget;
import { useTripStore } from "@/stores/trip/useTripStore";
import { User, Profile } from "@/types";
import { useAuthStore, useUtilsStore } from "@/stores";

const { trip: tripStore, budget: budgetStore } = useTripStore();
const { getTripDetails } = tripStore;
const { createExpense } = budgetStore;
const { trip } = getTripDetails();
const tripDateStart = computed(() => trip?.value?.start_date || null);
const tripDateEnd = computed(() => trip?.value?.end_date || null);
const { getTripId } = useUtilsStore();
const { members, isOwnerTrip } = defineProps<{
  isOwnerTrip: boolean;
  members: User[];
}>();

const { userData } = useAuthStore();
const { getUser } = userData;
const user = getUser();

const form = ref({
  title: "",
  amount: 0,
  currency: "PLN",
  date: tripDateStart.value,
  user: isOwnerTrip
    ? members[0]
    : user?.profiles?.find((e: Profile) => e.is_default)?.id,
  category: 1,
  note: "",
});

const emit = defineEmits(["cancelForm", "submitted"]);
const formRef = ref();
const hasError = ref(false);

const submitTicket = async () => {
  const isValid = await formRef.value?.validate?.();
  if (!isValid) {
    hasError.value = true;
    return;
  }
  hasError.value = false;

  createExpense.mutate(
    {
      trip: getTripId(),
      title: form.value.title,
      amount: form.value.amount,
      currency: form.value.currency,
      date: form.value.date
        ? new Intl.DateTimeFormat("pl-PL").format(new Date(form.value.date))
        : "",
      user:
        typeof form.value.user === "object" && "userId" in form.value.user
          ? form.value.user.userId
          : (form.value.user as number | undefined) ?? 0,
      category: form.value.category,
      note: form.value.note,
    },
    {
      onSuccess: () => {
        emit("submitted");
      },
    }
  );
};
const formIsValid = ref(false);
</script>

<template>
  <v-col cols="12">
    <v-form ref="formRef" v-slot="{ isValid }" v-model="formIsValid">
      <v-card class="ticket-form pa-3">
        <v-card-title>Dodaj nowy wydatek</v-card-title>
        <v-card-text>
          
          <v-row>
            <v-col cols="12" lg="6" md="6" class="tight-col">
              <v-select
                v-if="isOwnerTrip"
                v-model="form.user"
                :items="members"
                item-title="name"
                item-value="userId"
                label="Podaj uczestnika"
                variant="outlined"
                bg-color="background"
                density="comfortable"
                :rules="[(v) => !!v || 'Uczestnik jest wymagany']"
              />
              <v-text-field
                v-else
                :model-value="user?.fullname"
                label="Uczestnik"
                variant="outlined"
                bg-color="background"
                density="comfortable"
                readonly
                
              />
            </v-col>

            <v-col cols="12" lg="6" md="6" class="tight-col">
              <v-text-field
                v-model="form.title"
                label="Nazwa"
                variant="outlined"
                :rules="[(v) => !!v || 'Tytuł wydatku jest wymagany']"
                required
                prepend-inner-icon="mdi-text"
                bg-color="background"
                density="comfortable"
                clearable
              />
            </v-col>

            <v-col cols="12" lg="3" md="6" class="tight-col">
              <v-date-input
                required
                :min="tripDateStart"
                :max="tripDateEnd"
                :rules="[(v) => !!v || 'Data jest wymagana']"
                v-model="form.date"
                label="Wybierz datę"
                prepend-icon=""
                prepend-inner-icon="mdi-calendar"
                variant="outlined"
                :hide-actions="true"
                bg-color="background"
                density="comfortable"
                clearable
              />
            </v-col>

            <v-col cols="12" lg="3" md="6" class="tight-col">
              <v-text-field
                required
                min="0"
                :rules="[
                  (v) => !!v || 'Cena jest wymagana',
                  (v) => v > 0 || 'Cena musi być większa niż 0',
                  (v) => String(v).length <=5 || 'Cena jest zbyt duża',
                ]"
                v-model="form.amount"
                variant="outlined"
                label="Cena"
                prepend-inner-icon="mdi-currency-usd"
                bg-color="background"
                density="comfortable"
                type="number"
                clearable
              />
            </v-col>

            <v-col cols="12" lg="6" md="6" class="tight-col">
              <v-select
                required
                v-model="form.currency"
                label="Wybierz walutę"
                variant="outlined"
                :items="['EUR', 'GBP', 'USD', 'PLN']"
                :rules="[(v) => !!v || 'Wybierz walutę']"
                prepend-inner-icon="mdi-wallet"
                bg-color="background"
                density="comfortable"
              />
            </v-col>

            <v-col cols="12" lg="6" md="6" class="tight-col">
              <v-select
                required
                v-model="form.category"
                :items="categoryBudget"
                item-title="name"
                item-value="id"
                label="Wybierz kategorię"
                prepend-inner-icon="mdi-tag"
                variant="outlined"
                bg-color="background"
                density="comfortable"
                :rules="[(v) => !!v || 'Kategoria jest wymagana']"
              />
            </v-col>

            <v-col cols="12" lg="6" class="tight-col">
              <v-textarea
                v-model="form.note"
                label="Notatka"
                prepend-inner-icon="mdi-note"
                variant="outlined"
                bg-color="background"
                density="comfortable"
                :rules="[
                  (v) =>
                    !v ||
                    v.length <= 250 ||
                    'Notatka może mieć maks. 250 znaków',
                ]"
                clearable
              />
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions class="form-actions">
          <AppButton
            @click="$emit('cancelForm')"
            color="accent"
            text="Anuluj"
            font-auto
            height-auto
          />
          <AppButton
            color="primary"
            text="Dodaj"
            @click="submitTicket"
            font-auto
            height-auto
            :disabled="!formIsValid"
          />
        </v-card-actions>
      </v-card>
    </v-form>
  </v-col>
</template>

<style scoped lang="scss">
.ticket-form {
  background-color: rgb(var(--v-theme-secondary), 0.5);
  border-radius: 1rem;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25);
  margin: 0 auto;

  @media (max-width: 600px) {
    padding: 0.5rem !important;
  }
}

.form-actions {
  gap: 1rem;
  display: flex;
  justify-content: flex-end;
  @media (max-width: 600px) {
    flex-wrap: wrap;
    justify-content: center;
  }
}

.tight-col {
  padding: 0.25rem !important;
}
</style>

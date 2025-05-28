<script setup lang="ts">
import { ref } from "vue";
import AppButton from "@/components/AppButton.vue";
import { useTripStore } from "@/stores/trip/useTripStore";
import { User } from "@/types";
import {useUtilsStore} from "@/stores/utils/useUtilsStore";
const { getTripId } = useUtilsStore();
const { members } = defineProps<{
  isOwnerTrip: boolean;
  members: User[];
}>();

const form = ref<{
  title: string;
  name: string;
  amount: number;
  currency: string;
  user: number[];
}>({
  title: "",
  name: "",
  amount: 0,
  currency: "PLN",
  user: [],
});

const emit = defineEmits(["cancelForm", "submitted"]);
const formRef = ref();
const hasError = ref(false);
const {debt} = useTripStore();
const {createDebt} = debt;
const submitTicket = async () => {
  const isValid = await formRef.value?.validate?.();
  if (!isValid) {
    hasError.value = true;
    return;
  }
  hasError.value = false;

  createDebt.mutate(
    {
      trip: getTripId(),
      name: form.value.title,
      amount: form.value.amount,
      currency: form.value.currency,
      members:form.value.user
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
                v-model="form.user"
                :items="members"
                item-title="name"
                item-value="userId"
                label="Podaj uczestnika"
                variant="outlined"
                bg-color="background"
                density="comfortable"
                multiple
                chips
                :rules="[(v) => !!v || 'Uczestnik jest wymagany']"
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

            <v-col cols="12" lg="6" md="6" class="tight-col">
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

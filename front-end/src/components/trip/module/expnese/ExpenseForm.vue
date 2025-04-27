<script setup lang="ts">
import {ref, computed} from "vue";
import AppButton from "@/components/budget/AppButton.vue";
import {VDateInput} from "vuetify/labs/components";
import { budget } from "@/data/category/budget";

const categoryBudget = budget;
import {useTripStore} from "@/stores/trip/useTripStore";
const {getTripDetails, createExpense} = useTripStore();
import {useRoute} from "vue-router";
const tripId = useRoute().params.tripId as string;
const {data: tripData} = getTripDetails(Number(tripId));

const members = computed(() => {
  if (!tripData.value) return [];
  return [...(tripData.value?.members || []), ...(tripData.value?.pending_members || [])];
});
const form = ref({
  title:"",
  amount: 0,
  currency: "PLN",
  date: "",
  user: 0,
  category: 1,
  note: "",
});
const emit = defineEmits(["cancelForm"]);
const submitTicket = () =>{
  createExpense.mutate({
    trip: Number(tripId),
    title: form.value.title,
    amount: form.value.amount,
    currency: form.value.currency,
    date: new Date (form.value.date).toISOString().split("T")[0],
    user: form.value.user != 0 ? form.value.user : 2,
    category: form.value.category,
    note: form.value.note,
  });
}
</script>

<template>
  <v-card class="ticket-form pa-4 mt-4">
    <v-card-title>Dodaj nowy wydatek</v-card-title>

    <v-card-text>
      <v-row>
        <v-col cols="12" lg="6" md="6" class="tight-col">
          <v-select
              v-model="form.user"
              :items="members"
              item-title="name"
              item-value="id"
              label="Podaj uczestnika"
              variant="outlined"
              bg-color="background"
              density="comfortable"
              :disabled="members.length === 0"
          />
        </v-col>

        <v-col cols="12" lg="6" md="6" class="tight-col">
          <v-text-field
              v-model="form.title"
              label="Nazwa"
              variant="outlined"
              :rules="[v => !!v || 'Tytuł wydatku jest wymagana']"
              required
              prepend-inner-icon="mdi-text"
              bg-color="background"
              density="comfortable"
          />
        </v-col>

        <v-col cols="12" lg="3" md="6" class="tight-col">
          <v-date-input
              v-model="form.date"
              label="Wybierz datę"
              prepend-icon=""
              prepend-inner-icon="mdi-calendar"
              variant="outlined"
              :hide-actions=true
              :min="new Date().toISOString().split('T')[0]"
              bg-color="background"
              density="comfortable"
          />
        </v-col>

        <v-col cols="12" lg="3" md="6" class="tight-col">
          <v-text-field
              v-model="form.amount"
              variant="outlined"
              label="Cena"
              prepend-inner-icon="mdi-currency-usd"
              bg-color="background"
              density="comfortable"
              type="number"
          >
          </v-text-field>
        </v-col>


        <v-col cols="12" lg="6" md="6" class="tight-col">
          <v-select
              v-model="form.currency"
              label="Wybierz walute"
              variant="outlined"
              :items="['PLN', 'EUR']"
              clearable
              prepend-inner-icon="mdi-wallet"
              bg-color="background"
              density="comfortable"
          />
        </v-col>

        <v-col cols="12" lg="6" md="6" class="tight-col">
          <v-select
              class="custom-file-input"
              v-model="form.category"
              :items="categoryBudget"
              item-title="name"
              item-value="id"
              prepend-icon=""
              label="Wybierz kategorię"
              show-size
              prepend-inner-icon="mdi-tag"
              variant="outlined"
              bg-color="background"
              density="comfortable"
          >
          </v-select>
        </v-col>
        <v-col cols="12" lg="6" class="tight-col">
          <v-textarea
              class="custom-file-input"
              v-model="form.note"
              prepend-icon=""
              label="Notatka"
              show-size
              prepend-inner-icon="mdi-note"
              variant="outlined"
              bg-color="background"
              density="comfortable"
              >
          </v-textarea>
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-actions class="form-actions">
      <AppButton variant="secondary"
                 @click="$emit('cancelForm')">
        Anuluj
      </AppButton>
      <AppButton variant="primary" @click="submitTicket">
        Dodaj
      </AppButton>
    </v-card-actions>
  </v-card>
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

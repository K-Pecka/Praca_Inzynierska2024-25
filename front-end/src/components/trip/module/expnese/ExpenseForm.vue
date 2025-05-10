<script setup lang="ts">
import {computed, ref} from "vue";
import AppButton from "@/components/AppButton.vue";
import {VDateInput} from "vuetify/labs/components";
import { budget } from "@/data/category/budget";
const categoryBudget = budget;
import {useTripStore} from "@/stores/trip/useTripStore";
import { User } from "@/types";
import { useUtilsStore } from "@/stores";
const {trip:tripStore,createExpense} = useTripStore();
const {getTripDetails} = tripStore;
const {trip} = getTripDetails();
const tripDateStart = computed(()=>trip?.value?.end_date || '')

const {getTripId} = useUtilsStore();
const {members} = defineProps<{
  members: User[]
}>();
const form = ref({
  title: "",
  amount: 0,
  currency: "PLN",
  date: "",
  user: "",
  category: 1,
  note: "",
});
const emit = defineEmits(["cancelForm", "submitted"]);

const submitTicket = () => {
  createExpense.mutate({
    trip: getTripId(),
    title: form.value.title,
    amount: form.value.amount,
    currency: form.value.currency,
    date: new Intl.DateTimeFormat('pl-PL').format(new Date(form.value.date)),
    user: form.value.user !== "" ? Number(form.value.user) : members[0].userId,
    category: form.value.category,
    note: form.value.note,
  }, {
    onSuccess: () => {
      emit("submitted");
    }
  });
};

</script>

<template>
  <!-- <Section> -->
  <v-col cols="12">
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
                :max="tripDateStart"
                :min="new Date().toISOString().split('T')[0]"
                v-model="form.date"
                label="Wybierz datę"
                prepend-icon=""
                prepend-inner-icon="mdi-calendar"
                variant="outlined"
                :hide-actions=true
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
        />
      </v-card-actions>
    </v-card>
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

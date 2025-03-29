import { defineStore } from "pinia";
import { ref, computed } from "vue";

export interface Activity {
    id: string;
    type: string;
    name: string;
    date: string;
    startTime: string;
    duration: string;
    location?: string;
    assignedTo?: string;
    description?: string;
}

interface ActivityType {
    value: string;
    label: string;
    icon: string;
}

export const useActivityStore = defineStore("activity", () => {
    const activities = ref<Activity[]>([]);

    const activityTypes = ref<ActivityType[]>([
        { value: "tour", label: "Zwiedzanie", icon: "mdi-binoculars" },
        { value: "food", label: "Jedzenie", icon: "mdi-food" },
        { value: "sport", label: "Sport", icon: "mdi-basketball" },
        { value: "relax", label: "Relaks", icon: "mdi-beach" },
    ]);

    function addActivity(activityData: Omit<Activity, "id">) {
        const newActivity: Activity = {
            id: Date.now().toString(),
            ...activityData,
        };
        activities.value.push(newActivity);
    }

    function removeActivity(activityId: string) {
        activities.value = activities.value.filter((a) => a.id !== activityId);
    }

    const activitiesByDate = (date: string) =>
        computed(() => {
            return activities.value.filter((a) => a.date === date);
        });

    return {
        activities,
        activityTypes,
        addActivity,
        removeActivity,
        activitiesByDate,
    };
});

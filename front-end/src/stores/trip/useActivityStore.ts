import { defineStore } from "pinia";
import { ref, computed } from "vue";
import {
    useMutation,
    useQuery,
    useQueryClient
  } from "@tanstack/vue-query";
import { createActivity } from "@/api/trip/activity";
import router from "@/router";

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

    function addActivity(activityData: Activity,param: Record<string, string>={}) {
        // const newActivity: Activity = {
        //     id: Date.now().toString(),
        //     ...activityData,
        // };
        // console.log("Adding activity:", newActivity);
        // activities.value.push(newActivity);
        activityMutationAdd.mutate({activityData, param});
    }

    function removeActivity(activityId: string) {
        activities.value = activities.value.filter((a) => a.id !== activityId);
    }

    const activitiesByDate = (date: string) =>
        computed(() => {
            return activities.value.filter((a) => a.date === date);
        });
    const activityMutationAdd = useMutation({
        mutationFn: ({activityData,param}:{activityData:Activity,param:Record<string, string>}) => createActivity(activityData,param),
        onSuccess: (data) => {
        router.back();
        setSuccessCurrentMessage("dodano aktywność");
        },
        onError: (err) => {
        setErrorCurrentMessage("błąd");
        },
    });
    return {
        activities,
        activityTypes,
        addActivity,
        removeActivity,
        activitiesByDate,
    };
});
function setSuccessCurrentMessage(arg0: string) {
    throw new Error("Function not implemented.");
}

function setErrorCurrentMessage(arg0: string) {
    throw new Error("Function not implemented.");
}


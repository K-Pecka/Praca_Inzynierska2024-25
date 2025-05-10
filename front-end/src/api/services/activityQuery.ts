import { useQuery, useMutation } from "@tanstack/vue-query";
import { fetchActivities,fetchPlanDetails, createPlan, deleteItinerary } from "@/api";
import type { Activity } from "@/types";
import router from "@/router";
export const getActivitiesQuery = (tripId: string,planId:string) => 
  useQuery<Activity[], Error>({
        queryKey: ["activities", tripId, planId],
        queryFn: () => fetchActivities({ tripId: String(tripId), planId: String(planId) }),
      });
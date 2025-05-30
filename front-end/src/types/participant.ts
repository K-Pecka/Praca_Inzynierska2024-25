import type { Role } from './role';

export interface InvateUser {
  id: string;
  email: string;
}

export interface RoleSelection {
  title: string;
  subtitle: string;
  roles: Role[];
}

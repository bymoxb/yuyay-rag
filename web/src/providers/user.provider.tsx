import { createContext, useContext, useEffect, useState } from "react";
import { getUserByEmail } from "../services/user.service";

export type UserContextType = {
  profile: {
    email: string,
    fullName: string,
  },
  roles: string[],
  functionalities: string[],
}

export const UserContext = createContext<UserContextType>(null!);

type UserProviderProps = {} & React.PropsWithChildren;

export const UserProvider: React.FunctionComponent<UserProviderProps> = ({ children }) => {


  const [user, setUser] = useState<UserContextType>(null!);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    const fetchUser = async () => {
      const result = await getUserByEmail();

      if (result.ok) {
        setUser({
          profile: {
            fullName: result.data.fullName,
            email: result.data.email,
          },
          roles: result.data.roles,
          functionalities: result.data.functionalities,
        });
      } else {
        setUser(null!);
      }
      setLoading(false);

    }

    fetchUser();
  }, [])

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user?.profile?.email) {
    return <div>User not found</div>;
  }

  return (
    <UserContext.Provider value={user}>
      {children}
    </UserContext.Provider>
  )
}

export function useUserContext() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("useUserContext must be used within a UserProvider");
  }
  return context;
}

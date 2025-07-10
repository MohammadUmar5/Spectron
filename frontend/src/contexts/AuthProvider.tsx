import React, { createContext, useContext, useEffect, useState } from "react";
import { onAuthStateChanged, getAuth } from "firebase/auth";
import { doc, getDoc } from "firebase/firestore";
import { db } from "../services/config";

type AuthContextType = {
  isLoggedIn: boolean;
  hasProfile: boolean;
};

const AuthContext = createContext<AuthContextType>({
  isLoggedIn: false,
  hasProfile: false,
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [hasProfile, setHasProfile] = useState(false);
  const authInstance = getAuth();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(authInstance, async (user) => {
      if (user) {
        setIsLoggedIn(true);

        try {
          const userDocRef = doc(db, "users", user.uid);
          const userDoc = await getDoc(userDocRef);
          setHasProfile(userDoc.exists());
        } catch (error) {
          console.error("Error checking user profile:", error);
          setHasProfile(false); // fallback
        }
      } else {
        setIsLoggedIn(false);
        setHasProfile(false);
      }
    });

    return () => unsubscribe();
  }, []);

  return (
    <AuthContext.Provider value={{ isLoggedIn, hasProfile }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

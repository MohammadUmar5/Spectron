import {
  auth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  sendEmailVerification,
} from "./config";
  
import { signOut, type User } from "firebase/auth";
  
// Sign up with Email & Password
export const signupWithEmail = async (
  email: string,
  password: string
): Promise<User> => {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;

  // ✉️ Send email verification
  if (user) {
    await sendEmailVerification(user);
  }

  return user;
  } catch (error: unknown) {
    if (error instanceof Error) {
      console.error("Signup error:", error.message);
      throw new Error(error.message);
    }
    throw new Error("An unknown error occurred during signup.");
  }
};
  
// Login with Email & Password
export const loginWithEmail = async (
  email: string,
  password: string
): Promise<User> => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;

        // ✅ Check if email is verified
  if (!user.emailVerified) {
    // Optional: you can call user.sendEmailVerification() here if you want to resend
    throw new Error("Please verify your email before logging in.");
  }

  return user;
  } catch (error: unknown) {
    if (error instanceof Error) {
      console.error("Login error:", error.message);
      throw new Error(error.message);
    }
    throw new Error("An unknown error occurred during login.");
  }
};
  
  // Logout function
export const logout = async (): Promise<void> => {
  try {
    await signOut(auth); // Sign out the current user
    console.log("User logged out successfully.");
  } catch (error: unknown) {
    if (error instanceof Error) {
      console.error("Logout error:", error.message);
      throw new Error(error.message);
    }
    throw new Error("An unknown error occurred during logout.");
  }
};
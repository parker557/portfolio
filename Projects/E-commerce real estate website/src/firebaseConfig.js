// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY || "replace-with-firebase-api-key",
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN || "replace-with-firebase-auth-domain",
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID || "replace-with-firebase-project-id",
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET || "replace-with-firebase-storage-bucket",
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID || "replace-with-firebase-messaging-sender-id",
  appId: process.env.REACT_APP_FIREBASE_APP_ID || "replace-with-firebase-app-id"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const firestore = getFirestore(app);
// Initialize Firebase Authentication and get a reference to the service
// export default app;
export {auth,firestore};

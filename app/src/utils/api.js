import { useKayakStore } from "@/store";
import { deferred } from "./deferred";


const locationNames = [
  "Lake Union",
  "Green Lake",
  "Seward Park",
  "Matthews Beach Park",
  "Lake Sammamish"
];

// Define the base URL for your API endpoints
const API_BASE_URL = import.meta.env.API_BASE_URL || "https://kayak-backend-78192108242.us-central1.run.app/api";

const promptTemplate = (prompt) => {
  return `
    You are an expert kayak guide. 
    A user has requested the following: ${prompt}. 
    Provide a detailed plan for a kayak trip that fulfills the user's request.
  `;
};

let sendPromptPromise = null;

export const sendPrompt = async () => {
  if (sendPromptPromise) {
    return sendPromptPromise;
  }

  const { prompt } = useKayakStore();

  console.log("Initial prompt", prompt);

  if (!prompt) return;

  const defer = deferred();
  sendPromptPromise = defer;

  try {
    // Step 1: Send the initial prompt to get intermediate data
    const promptResponse = await fetch(`${API_BASE_URL}/process-prompt`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    });

    if (!promptResponse.ok) {
      throw new Error(`HTTP error during prompt processing! status: ${promptResponse.status}`);
    }

    const promptData = await promptResponse.json();
    console.log("Prompt processing data", promptData);

    useKayakStore().setLocation({
      name: promptData.location,
      location_id: promptData.location_id,
      description: promptData.description, // "The lighthouse keeper, Silas, was a man woven from the sea itself. His skin was tanned and weathered like driftwood, his eyes the grey-green of a stormy horizon, and his beard, a tangled mess of white and salt, whispered secrets of the deep. He'd been tending the beacon on Gull Island for forty years, a solitary sentinel against the relentless ocean.",
      image: promptData.image_url, //"/images/kayak/image-grid-1.jpg",
    });

    sendPromptPromise.resolve();
  } catch (error) {
    console.error("Error during prompt and location processing:", error);
    sendPromptPromise.reject(error);
  } finally {
    sendPromptPromise = null;
  }
};  

let moveKayakAndGetCodePromise = null;
export const moveKayakAndGetCode = async () => {
  if (moveKayakAndGetCodePromise) {
    return moveKayakAndGetCodePromise;
  }

  const defer = deferred();
  moveKayakAndGetCodePromise = defer;
  const { prompt, location_id , location } = useKayakStore();
  useKayakStore().setIsMoving(true);

  // Get Code API Call
  const codeResponse = await fetch(`${API_BASE_URL}/get-code`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({prompt, location_id, location}), // Add any necessary data for getting the code
  });

  if (!codeResponse.ok) {
    throw new Error(`HTTP error! status: ${codeResponse.status}`);
  }

  const codeData = await codeResponse.json();
  const code = codeData.code;

  // Simulate a stream response
  for (let i = 0; i < code.length; i++) {
    useKayakStore().setCode(code.slice(0, i + 1));
    await new Promise((resolve) => setTimeout(resolve, 5));
  }

  try {
    // Move Kayak API Call
    const moveResponse = await fetch(`${API_BASE_URL}/move-kayak`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ location, location_id }),
    });

    if (!moveResponse.ok) {
      throw new Error(`HTTP error! status: ${moveResponse.status}`);
    }
    
    moveKayakAndGetCodePromise.resolve();
  } catch (error) {
    console.error("Error moving kayak or getting code:", error);
    moveKayakAndGetCodePromise.reject(error);
  } finally {
    moveKayakAndGetCodePromise = null;
  }
};

let isKayakArrivedPromise = null;
export const checkIfKayakArrived = async () => {
  if (isKayakArrivedPromise) {
    return isKayakArrivedPromise;
  }

  const defer = deferred();
  isKayakArrivedPromise = defer;

  let interval = null;
  let debugMaxTries = 4;
  let debugTries = 0;

  const isKayakArrived = () => {
    // TODO: implement this
    // fetch(...)
    // if (/* kayak has arrived */) {

    if (debugTries >= debugMaxTries) {
      clearInterval(interval);
      useKayakStore().setArrived(true);
      isKayakArrivedPromise.resolve(true);
      isKayakArrivedPromise = null;
      return;
    }

    debugTries++;
    console.log("debugTries", debugTries);
  }


  interval = setInterval(isKayakArrived, 1000);

  await new Promise((resolve) => setTimeout(resolve, 1000));
};


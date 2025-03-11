import { useKayakStore } from "@/store";
import { deferred } from "./deferred";

const locationNames = [
  "Lake Union",
  "Green Lake",
  "Lake Washington (Seward Park)",
  "Lake Washington (Matthews Beach Park)",
  "Lake Sammamish"
];

let sendPromptPromise = null;

export const sendPrompt = async () => {
  if (sendPromptPromise) {
    return sendPromptPromise;
  }

  const { prompt } = useKayakStore();

  console.log("prompt", prompt);

  if (!prompt) return;

  const defer = deferred();
  sendPromptPromise = defer;

  // TODO: implement this
  // fetch(...)

  await new Promise((resolve) => setTimeout(resolve, 3000));

  const locationName = locationNames[Math.floor(Math.random() * locationNames.length)];

  useKayakStore().setLocation({
    name: locationName,
    description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image: "/images/kayak/image-grid-1.jpg",
  });

  sendPromptPromise.resolve();
  sendPromptPromise = null;
}